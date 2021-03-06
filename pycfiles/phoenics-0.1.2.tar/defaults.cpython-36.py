# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/flo/Phoenics/master/src/phoenics/utilities/defaults.py
# Compiled at: 2019-11-24 12:43:13
# Size of source mod 2**32: 2660 bytes
"""
Licensed to the Apache Software Foundation (ASF) under one or more 
contributor license agreements. See the NOTICE file distributed with this 
work for additional information regarding copyright ownership. The ASF 
licenses this file to you under the Apache License, Version 2.0 (the 
"License"); you may not use this file except in compliance with the 
License. You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
License for the specific language governing permissions and limitations 
under the License.

The code in this file was developed at Harvard University (2018) and 
modified at ChemOS Inc. (2019) as stated in the NOTICE file.
"""
__author__ = 'Florian Hase'
default_general_configurations = {'backend':'tfprob', 
 'batches':1, 
 'boosted':True, 
 'parallel':True, 
 'random_seed':100691, 
 'sampler':'uniform', 
 'sampling_strategies':2, 
 'scratch_dir':'./.scratch', 
 'softness':0.001, 
 'continuous_optimizer':'adam', 
 'categorical_optimizer':'naive', 
 'discrete_optimizer':'naive', 
 'verbosity':{'default':2, 
  'bayesian_network':3, 
  'random_sampler':2}}
default_database_configurations = {'format':'sqlite', 
 'path':'./SearchProgress', 
 'log_observations':True, 
 'log_runtimes':True}
default_configuration = {'general':{key:default_general_configurations[key] for key in default_general_configurations.keys()}, 
 'database':{key:default_database_configurations[key] for key in default_database_configurations.keys()}, 
 'parameters':[
  {'name':'param_0', 
   'type':'continuous',  'low':0.0,  'high':10.0,  'size':2},
  {'name':'param_1', 
   'type':'continuous',  'low':-1.0,  'high':1.0,  'size':1}], 
 'objectives':[
  {'name':'obj_0', 
   'goal':'minimize',  'hierarchy':0,  'tolerance':0.2},
  {'name':'obj_1', 
   'goal':'maximize',  'hierarchy':1,  'tolerance':0.2}]}