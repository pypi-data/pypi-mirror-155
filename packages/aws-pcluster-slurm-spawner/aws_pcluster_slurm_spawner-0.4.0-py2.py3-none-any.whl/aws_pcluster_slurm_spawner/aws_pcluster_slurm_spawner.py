"""Main module."""

import os
import json

import shlex

import functools
from pprint import pprint
from slugify import slugify
import batchspawner
from jupyterhub.spawner import LocalProcessSpawner
from jinja2 import Environment, BaseLoader
from jupyterhub.spawner import Spawner
from traitlets import Integer, Unicode, Float, Dict, default
from traitlets import (
    Bool,
    Dict,
    Integer,
    List,
    Unicode,
    Union,
    default,
    observe,
    validate,
)

from typing import List, Union
from datasize import DataSize
import humanize
from dataclasses import dataclass
from pathlib import Path
import boto3
import os
# from aws_pcluster_helpers import (SinfoRow, SInfoTable)
from aws_pcluster_helpers.models.sinfo import (SInfoTable, SinfoRow)

pcluster_spawner_template_paths = os.path.join(os.path.dirname(__file__), 'templates')


class PClusterSlurmSpawner(batchspawner.SlurmSpawner):
    batch_script = Unicode("""#!/bin/bash
#SBATCH --output={{homedir}}/jupyterhub_slurmspawner_%j.log
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --chdir={{homedir}}
#SBATCH --export={{keepvars}}
#SBATCH --get-user-env=L
{% if req_partition  %}#SBATCH --partition={{req_partition}}{% endif %}
{% if req_constraint %}#SBATCH --constraint={{req_constraint}}{% endif %}
{% if req_nprocs %}#SBATCH --cpus-per-task={{req_nprocs}}{% endif %}
{% if exclusive %}#SBATCH --exclusive{% endif %}
{% if runtime    %}#SBATCH --time={{runtime}}{% endif %}
{% if options    %}#SBATCH {{options}}{% endif %}
set -euo pipefail
trap 'echo SIGTERM received' TERM

{{prologue}}

# Custom R
{% if req_custom_r    %}export PATH="{{req_custom_r}}:$PATH"{% endif %}

which jupyterhub-singleuser
{% if srun %}{{srun}} {% endif %}{{cmd}}
echo "jupyterhub-singleuser ended gracefully"
{{epilogue}}
    """)

    profile_form_template = Unicode(
        """
        <style>
            /*
                .profile divs holds two div tags: one for a radio button, and one
                for the profile's content.
            */
            #pclusterslurmspawner-profiles-list .profile {
                display: flex;
                flex-direction: row;
                font-weight: normal;
                border-bottom: 1px solid #ccc;
                padding-bottom: 12px;
            }
            #pclusterslurmspawner-profiles-list .profile .radio {
                padding: 12px;
            }
            /* .option divs holds a label and a select tag */
            #pclusterslurmspawner-profiles-list .profile .option {
                display: flex;
                flex-direction: row;
                align-items: center;
                padding-bottom: 12px;
            }
            #pclusterslurmspawner-profiles-list .profile .option label {
                font-weight: normal;
                margin-right: 8px;
                min-width: 96px;
            }
        </style>
        <div class='form-group' id='pclusterslurmspawner-profiles-list'>
            {%- for profile in profile_list %}
            {#- Wrap everything in a <label> so clicking anywhere selects the option #}
            <label for='profile-item-{{ profile.slug }}' class='profile'>
                <div class='radio'>
                    <input type='radio' name='profile' id='profile-item-{{ profile.slug }}' value='{{ profile.slug }}' {% if profile.default %}checked{% endif %} required />
                </div>
                <div>
                    <h3>{{ profile.display_name }}</h3>
                    {%- if profile.description %}
                    <p>{{ profile.description }}</p>
                    {%- endif %}
                    {%- if profile.profile_options %}
                    <div>
                        {%- for k, option in profile.profile_options.items() %}
                        <div class='option'>
                            <label for='profile-option-{{profile.slug}}-{{k}}'>{{option.display_name}}</label>
                            <select name="profile-option-{{profile.slug}}-{{k}}" class="form-control">
                                {%- for k, choice in option['choices'].items() %}
                                <option value="{{ k }}" {% if choice.default %}selected{%endif %}>{{ choice.display_name }}</option>
                                {%- endfor %}
                            </select>
                        </div>
                        {%- endfor %}
                    </div>
                    {%- endif %}
                </div>
            </label>
            {%- endfor %}
        </div>
        """,
        config=True,
        help="""
        Jinja2 template for constructing profile list shown to user.
        Used when `profile_list` is set.
        The contents of `profile_list` are passed in to the template.
        This should be used to construct the contents of a HTML form. When
        posted, this form is expected to have an item with name `profile` and
        the value the index of the profile in `profile_list`.
        """,
    )

    _profile_list = None

    def _init_profile_list(self, profile_list):
        # generate missing slug fields from display_name
        for profile in profile_list:
            if 'slug' not in profile:
                profile['slug'] = slugify(profile['display_name'])

        return profile_list

    def _render_options_form(self, profile_list):
        self._profile_list = self._init_profile_list(profile_list)
        profile_form_template = Environment(loader=BaseLoader).from_string(
            self.profile_form_template
        )
        return profile_form_template.render(profile_list=self._profile_list)

    @property
    def profiles_list(self) -> List[Dict]:
        """
        List of profiles to offer for selection by the user.
        Signature is: `List(Dict())`, where each item is a dictionary that has two keys:
        - `display_name`: the human readable display name (should be HTML safe)
        - `slug`: the machine readable slug to identify the profile
          (missing slugs are generated from display_name)
        - `description`: Optional description of this profile displayed to the user.
        - `pclusterslurmspawner_override`: a dictionary with overrides to apply to the PClusterSlurmSpawner
          settings. Each value can be either the final value to change or a callable that
          take the `PClusterSlurmSpawner` instance as parameter and return the final value. This can
          be further overridden by 'profile_options'
        - 'profile_options': A dictionary of sub-options that allow users to further customize the
          selected profile. By default, these are rendered as a dropdown with the label
          provided by `display_name`. Items should have a unique key representing the customization,
          and the value is a dictionary with the following keys:
          - 'display_name': Name used to identify this particular option
          - 'choices': A dictionary containing list of choices for the user to choose from
            to set the value for this particular option. The key is an identifier for this
            choice, and the value is a dictionary with the following possible keys:
            - 'display_name': Human readable display name for this choice.
            - 'default': (optional Bool) True if this is the default selected choice
            - 'pclusterslurmspawner_override': A dictionary with overrides to apply to the PClusterSlurmSpawner
              settings, on top of whatever was applied with the 'pclusterslurmspawner_override' key
              for the profile itself. The key should be the name of the pclusterslurmspawner setting,
              and value can be either the final value or a callable that returns the final
              value when called with the spawner instance as the only parameter.
        - `default`: (optional Bool) True if this is the default selected option
        pclusterslurmspawner setting overrides work in the following manner, with items further in the
        list *replacing* (not merging with) items earlier in the list:
        1. Settings directly set on PClusterSlurmSpawner, via c.PClusterSlurmSpawner.<traitlet_name>
        2. `pclusterslurmspawner_override` in the profile the user has chosen
        3. `pclusterslurmspawner_override` in the specific choices the user has made within the
           profile, applied linearly based on the ordering of the option in the profile
           definition configuration
        Example::
            c.PClusterSlurmSpawner.profile_list = [
                {
                    'display_name': 'Training Env',
                    'slug': 'training-python',
                    'default': True,
                    'profile_options': {
                        'image': {
                            'display_name': 'Image',
                            'choices': {
                                'pytorch': {
                                    'display_name': 'Python 3 Training Notebook',
                                    'pclusterslurmspawner_override': {
                                        'image': 'training/python:2022.01.01'
                                    }
                                },
                                'tf': {
                                    'display_name': 'R 4.2 Training Notebook',
                                    'pclusterslurmspawner_override': {
                                        'image': 'training/r:2021.12.03'
                                    }
                                }
                            }
                        }
                    },
                    'pclusterslurmspawner_override': {
                        'cpu_limit': 1,
                        'mem_limit': '512M',
                    }
                }, {
                    'display_name': 'Python DataScience',
                    'slug': 'datascience-small',
                    'profile_options': {
                        'memory': {
                            'display_name': 'CPUs',
                            'choices': {
                                '2': {
                                    'display_name': '2 CPUs',
                                    'pclusterslurmspawner_override': {
                                        'cpu_limit': 2,
                                        'cpu_guarantee': 1.8,
                                        'node_selectors': {
                                            'node.kubernetes.io/instance-type': 'n1-standard-2'
                                        }
                                    }
                                },
                                '4': {
                                    'display_name': '4 CPUs',
                                    'pclusterslurmspawner_override': {
                                        'cpu_limit': 4,
                                        'cpu_guarantee': 3.5,
                                        'node_selectors': {
                                            'node.kubernetes.io/instance-type': 'n1-standard-4'
                                        }
                                    }
                                }
                            }
                        },
                    },
                    'pclusterslurmspawner_override': {
                        'image': 'datascience/small:label',
                    }
                }, {
                    'display_name': 'DataScience - Medium instance (GPUx2)',
                    'slug': 'datascience-gpu2x',
                    'pclusterslurmspawner_override': {
                        'image': 'datascience/medium:label',
                        'cpu_limit': 48,
                        'mem_limit': '96G',
                        'extra_resource_guarantees': {"nvidia.com/gpu": "2"},
                    }
                }
            ]
        Instead of a list of dictionaries, this could also be a callable that takes as one
        parameter the current spawner instance and returns a list of dictionaries. The
        callable will be called asynchronously if it returns a future, rather than
        a list. Note that the interface of the spawner class is not deemed stable
        across versions, so using this functionality might cause your JupyterHub
        or pclusterslurmspawner upgrades to break.

        In [16]:  sinfo.dataframe.groupby('queue').get_group('mem')
        Out[16]:
                  sinfo_name                label queue  constraint ec2_instance_type  mem  cpu   gpu gpus extra
        6  mem-dy-r6i2xlarge  mem_dy__r6i_2xlarge   mem  r6i2xlarge       r6i.2xlarge   64    4  None   []    {}
        5  mem-dy-m5a4xlarge  mem_dy__m5a_4xlarge   mem  m5a4xlarge       m5a.4xlarge   64    8  None   []    {}
        7  mem-dy-c6a8xlarge  mem_dy__c6a_8xlarge   mem  c6a8xlarge       c6a.8xlarge   64   16  None   []    {}
        """
        groups = self.sinfo.dataframe.groupby('queue').groups
        profiles = []
        for key in groups.keys():
            group = self.sinfo.dataframe.groupby('queue').get_group(key)
            profile = {
                'display_name': f'Queue: {key}',
                'slug': key,
                'ami_name': 'Deep Learning',
                'profile_options': {
                    'instance_types': {
                        'display_name': 'Instance Types',
                        'choices': {
                        }
                    },
                },
            }
            for group_record in group.to_dict('records'):
                sinfo_name = group_record['sinfo_name']
                instance_type = group_record['ec2_instance_type']

                mem = group_record['mem']
                cpu = group_record['cpu']
                profile['profile_options']['instance_types']['choices'][sinfo_name] = dict(
                    display_name=f'{instance_type} - {cpu} CPU, {mem} GB',
                    pclusterslurmspawner_override=group_record,
                )

            profiles.append(profile)
        return profiles

    @property
    def sinfo(self):
        return SInfoTable()

    @property
    def slurm_spawner_html_table(self):
        table = self.sinfo.dataframe

        return table.to_html(table_id="slurm_spawner_table",
                             classes='table  table-bordered display dataTable',
                             columns=['sinfo_name', 'queue', 'constraint', 'ec2_instance_type', 'mem', 'cpu',
                                      'gpus'], index=False)

    def _options_form_default(self):
        sinfo = SInfoTable()
        table = sinfo.dataframe
        profile_form = None
        try:
            profile_form = self._render_options_form(self.profiles_list)
        except Exception as e:
            self.log.error('Got an error rendering the profiles list')
            self.log.error(e)
        if table.shape[0]:
            first_row: SinfoRow = table.iloc[0]

            defaults = {
                'req_nprocs': str(first_row.cpu),
                'req_memory': str(first_row.mem),
                'req_runtime': "01:00:00",
                'req_partition': first_row.queue,
                'req_options': '',
                'req_custom_r': '',
                'req_constraint': first_row.constraint,
                'exclusive': True,
                # 'slurm_spawner_table': html_table,
                'slurm_spawner_table': '',
                'profile': profile_form,
            }
        else:
            # TODO If there's nothing in the table we have a problem
            defaults = {
                'slurm_spawner_table': '',
                # 'slurm_spawner_table': html_table,
                'profile': profile_form,
            }

        form_options = """
<div class="form-group">
    <label for="slurm_spawner_table">SLURM Options</label>
    {{slurm_spawner_table}}
</div>

{{profile}}

<input type="checkbox" id="exclusive" name="exclusive" value="exclusive" {% if exclusive %}checked{%endif %}>

<label for="exclusive"> Exclusive (Reserve the entire node)</label><br>
<div class="form-group">
    <label for="runtime">Runtime (--time)</label>
    <input type="text" class="form-control" value="{{req_runtime}}" placeholder="{{req_runtime}}" id="runtime" name="req_runtime"/>
</div>

<div class="form-group">
    <label for="options">Options (additional options such as -N 4 for multiple nodes)</label>
    <input type="text" class="form-control" value="{{req_options}}" placeholder="{req_options}" id="options" name="req_options"/>
</div>

<div class="form-group">
    <label for="custom_r_path">Custom R Path (Run source activate my-r-env; which R)</label>
    <input type="text" class="form-control" value="{{req_custom_r}}" placeholder="" id="custom_r" name="req_custom_r"/>
</div>
    """
        rtemplate = Environment(loader=BaseLoader).from_string(form_options)
        return rtemplate.render(**defaults)

    def options_from_form(self, formdata):
        submission_data = {}

        # self.log.debug('--------------------------------')
        # self.log.debug('FORM DATA')
        # self.log.debug(formdata)
        # self.log.debug('--------------------------------')
        # self.log.debug('USER OPTIONS')
        # self.log.debug(self.user_options)
        # self.log.debug('-------------------------------')
        queue = formdata['profile'][0]
        sinfo_name = formdata[f'profile-option-{queue}-instance_types'][0]
        records = self.sinfo.dataframe.loc[self.sinfo.dataframe['sinfo_name'] == sinfo_name].to_dict('records')
        record = records[0]
        for key in formdata.keys():
            form_value = formdata.get(key, [''])
            if not form_value[0]:
                if key in self.user_options:
                    form_value[0] = self.user_options[key]

            submission_data[key] = form_value[0]

        submission_data['req_nprocs'] = str(record['cpu'])
        submission_data['req_memory'] = str(record['mem'])
        submission_data['req_partition'] = record['queue']
        submission_data['req_constraint'] = record['constraint']

        for key in submission_data.keys():
            setattr(self, key, submission_data[key])

        if 'req_custom_r' in submission_data.keys():
            custom_r = submission_data['req_custom_r']
            custom_r = os.path.split(custom_r)
            if custom_r[1] == 'R':
                custom_r = custom_r[0]
            else:
                custom_r = os.path.join(custom_r[0], custom_r[1])
            submission_data['req_custom_r'] = custom_r

        if 'exclusive' in submission_data.keys():
            submission_data['exclusive'] = True
        else:
            submission_data['exclusive'] = False

        self.log.debug('-------------------------------')
        self.log.debug('SUBMISSION_DATA')
        self.log.debug(submission_data)

        return submission_data
