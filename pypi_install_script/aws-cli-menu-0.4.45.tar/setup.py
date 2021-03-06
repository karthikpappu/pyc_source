import sys
import os
from setuptools import setup, find_packages

SRC_DIR = 'src'

PREFIX = '/usr/share/aws-cli-menu'

def readme():
    with open('README.rst') as f:
        return f.read()


def get_version():
    sys.path[:0] = [SRC_DIR]
    return __import__('aws_cli_menu').__version__

if "VIRTUAL_ENV" in os.environ:
        # could be a virtual environment
        virtual = os.environ('VIRTUAL_ENV')




if ('virtual' in vars() or 'virtual' in globals()) and len(virtual)>0:

    PREFIX = str(virtual)+str(PREFIX)

    if not os.path.exists(str(virtual)+'/usr/share/'):
            os.makedirs(str(virtual)+'/usr/share/')

    if os.path.exists('/usr/share/aws-cli-menu'):
        for root, dirs, files in os.walk(str(virtual)+'/usr/share/aws-cli-menu', topdown=False):
                for name in files:
                        os.remove(os.path.join(root, name))
                for name in dirs:
                        os.rmdir(os.path.join(root, name))

else:

    if os.path.exists('/usr/share/aws-cli-menu'):
        for root, dirs, files in os.walk('/usr/share/aws-cli-menu', topdown=False):
                for name in files:
                        os.remove(os.path.join(root, name))
                for name in dirs:
                        os.rmdir(os.path.join(root, name))


setup(
    name='aws-cli-menu',
    version='0.4.45',
    author='Will Rubel',
    maintainer='Will Rubel',
    maintainer_email='willrubel@gmail.com',
    description='Menu system for Managing AWS Accounts',
    long_description=readme(),
    author_email='willrubel@gmail.com',
    license='Apache 2.0 License',
    keywords='AWS CLI AWSCLI Boto Boto3',
    url='https://rubelw@bitbucket.org/rubelw/aws_cli_menu.git',
    install_requires=[
        'boto3',
        'pyyaml',
        'six',
        'jinja2' + (' == 2.6' if sys.version_info[:2] == (3, 2) else ''),
    ],
    tests_require=[
        'mock == 1.0.1',  # lock version for older version of setuptools
    ] + (['unittest2'] if sys.version_info < (2, 7) else []),
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR),
    include_package_data=True,
    test_suite='tests',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Systems Administration'
    ],
    entry_points="""
    [console_scripts]
    aws-cli-menu = aws_cli_menu.aws_cli_menu:main
    """,
    data_files =    [
            (PREFIX, ['datafiles/aws-cli-menu.yml']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_public_dns_names.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_public_ips.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_private_ips.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_security_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_availability_zones.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_s3_buckets.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_undeleted_stack.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_resources.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_policies.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_vpc_peering_connections.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_subnets.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_ec2_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_users.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_policies_attached_to_user.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_roles.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_hosted_zones.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_resource_record_sets.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_database_clusters.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_route_tables.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/lookup_vpc_info.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_subnets_for_vpc.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_all_vpcs.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_all_subnets.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_vpc.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_vpc.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_subnet.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_subnet.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_tags.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_tags.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_peering_connection.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_account_aliases.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_peering_connections.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/accept_peering_connections.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_peering_connections.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_elastic_ips.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_endpoints.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_internet_gateways.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_network_acls.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_sns_subscriptions.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_sqs_queues.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_available_images.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_key_pairs.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_account_attributes.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_elastic_load_balancers.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_auto_scaling_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_auto_scaling_instances.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_auto_scaling_load_balancers.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_auto_scaling_termination_policy_types.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_auto_scaling_policies.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_auto_scaling_activities.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_auto_scaling_launch_configurations.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_auto_scaling_lifecycle_hooks.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_auto_scaling_notification_configurations.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_auto_scaling_scheduled_actions.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_cloud_watch_alarms.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_s3_bucket_acl.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_volume.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_volumes.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/find_ec2_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_volume.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_key_pair.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_key_pair.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/stop_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_internet_gateway.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/attach_internet_gateway.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/detach_internet_gateway.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_internet_gateway.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_iam_user.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_iam_user.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_iam_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_iam_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/get_iam_user_group_policy.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/attach_policy_to_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_policies_attached_to_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/detach_policy_from_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/attach_policy_to_user.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/detach_policy_from_user.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/attach_policy_to_role.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_iam_role.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/detach_policy_from_role.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_iam_role.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_iam_policy.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_dynamo_dbs.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_dynamodb_table.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_dynamodb_table.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_dynamodb_table.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_vpcs.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_tags.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_rds_instances.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_rds_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_rds_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_rds_snapshots.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_network_acl.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_network_acl.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_network_acl_entries.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/add_network_acl_entry.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_network_acl_entry.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_network_acls_subnet_associations.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/change_network_acl_subnet_association.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_elastic_ip.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_elastic_ip.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/associate_elastic_ip.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/disassociate_elastic_ip.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_customer_managed_policies.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_iam_customer_managed_policies.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_elastic_load_balancer.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_server_certificates.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/upload_iam_server_certificates.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_iam_server_certificates.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_elastic_load_balancer.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/attach_instance_to_elastic_load_balancer.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/get_cf_template_for_stack.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_s3_file_url.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/get_s3_bucket_policy.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_sns_topic.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_sns_topic.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_sns_topics.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_sns_subscription.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_route53_traffic_policies.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_route53_geo_locations.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_sqs_queue.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_sqs_queue.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/purge_sqs_queue.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/send_message_to_sqs_queue.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/receive_message_from_sqs_queue.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/change_map_public_ip_on_launch_for_subnet.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_security_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_security_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_nat_gateways.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_nat_gateway.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_nat_gateway.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_network_interfaces.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_policies_attached_to_role.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_user_access_keys.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_iam_user_access_key.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_iam_user_access_key.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_user_login_profile.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_iam_user_login_profile.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_iam_user_login_profile.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_customer_managed_policy_versions.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_new_iam_customer_managed_policy_version.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_iam_customer_managed_policy_version.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_user_mfa_devices.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_virtual_mfa_device.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/deactivate_user_mfa_device.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_user_mfa_device.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_user_virtual_mfa_devices.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_user_virtual_mfa_device.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_support_cases.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/allocate_address_for_elastic_ip.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_addresses.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_hosts.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/detach_volume.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/attach_volume.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_network_interface.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/attach_network_interface.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/detach_network_interface.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_network_interface.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_dhcp_options.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_dhcp_option.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_dhcp_option.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/associate_dhcp_option_to_vpc.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_route_table_for_vpc.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/disassociate_route_table_from_subnet.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/associate_route_table_to_subnet.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_all_route_tables.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_route_table.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_snapshots.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/start_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_snapshot_of_volume.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_snapshot_of_volume.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/enable_ec2_instance_monitoring.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/disable_ec2_instance_monitoring.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_rds_snapshot.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_rds_snapshot.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_user_policies.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_instance_profiles.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_ssh_public_keys.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_signing_certificates.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_saml_providers.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_iam_open_id_connect_providers.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_customer_gateways.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_ec2_reserved_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_ec2_spot_instance_requests.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/reset_ec2_instance_attribute.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_iam_account_alias.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_iam_account_alias.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/disable_cloud_watch_alarm.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/enable_cloud_watch_alarm.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_cloud_watch_alarm.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_cloud_watch_alarm.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/modify_rds_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_rds_security_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_rds_security_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_rds_security_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/authorize_rds_security_group_ingress.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/revoke_rds_security_group_ingress.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_rds_parameter_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_rds_subnet_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_rds_subnet_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_security_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_clusters.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_engine_versions.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_parameter_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_parameters.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_subnet_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_engine_default_parameters.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_events.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_replication_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_reserved_nodes.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_reserved_nodes_offerings.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_elastic_cache_snapshots.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_elastic_cache_security_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_elastic_cache_security_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_elastic_cache_replication_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_elastic_cache_cluster.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_elastic_cache_parameter_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_elastic_cache_parameter_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_elastic_cache_subnet_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_placement_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_placement_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_placement_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_launch_configurations.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_launch_configuration.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_launch_configuration.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_spot_instance_requests.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_spot_price_history.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_spot_fleet_request.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_spot_fleet_instances.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_reserved_instances.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_reserved_instance_offerings.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_reserved_instance_modifications.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/reboot_rds_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_vpn_connections.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_vpn_gateways.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_vpn_gateway.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_vpn_gateway.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_vpn_connection.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_customer_gateway.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_customer_gateway.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_vpn_connection.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_rest_apis.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_rest_api.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_rest_api.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/modify_hosts.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/release_host.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/ec2_dashboard.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_ec2_running_instances.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/rds_dashboard.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_reserved_rds_instances.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_manual_rds_snapshots.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_automated_rds_snapshots.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_rds_events.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_rds_event_subscriptions.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_rds_option_groups.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/vpc_dashboard.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/ec2_uptime_30_days_or_more.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/volumes_have_a_specific_tag.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/detached_volumes_30_days_or_more.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/determine_if_rds_snapshot_is_shared.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/determine_if_rds_snapshot_exists.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/get_private_ip_for_ec2_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/determine_if_ec2_instance_exists.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/determine_rds_security_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/change_rds_security_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/copy_shared_rds_snapshot.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_ecs_clusters.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_ecs_tasks.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_ecs_services.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_ecs_container_instances.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_ecs_cluster.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_ecs_cluster.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/register_ecs_container_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_ecs_instance.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_ecs_instance_role.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_ecs_service_role.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_ecs_security_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_ecs_launch_configuration.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_ecs_auto_scaling_group.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/register_ecs_task_definition.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_ecs_inactive_task_definitions.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_ecs_task_definition_families.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_ecs_service.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/describe_ecs_task_definitions.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/list_ecs_active_task_definitions.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/delete_ecs_service.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/stop_ecs_task.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/stop_ecs_service.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/start_ecs_service.py']),
            (PREFIX+'/scripts', ['datafiles/scripts/create_cf_stack.py'])


    ]
)
