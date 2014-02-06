from django.conf.urls import patterns, url

from djsopnet import views

# Sopnet API
urlpatterns += patterns('',
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/setup_blocks$', 'catmaid.control.setup_blocks'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/block_at_location$', 'catmaid.control.block_at_location'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/block$', 'catmaid.control.block_info'),

     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/segment_flag$', 'catmaid.control.set_block_segment_flag'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/slice_flag$', 'catmaid.control.set_block_slice_flag'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/insert_slice$', 'catmaid.control.insert_slice'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/slices_block$', 'catmaid.control.set_slices_block'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/slices_by_hash$', 'catmaid.control.retrieve_slices_by_hash'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/slices_by_id$', 'catmaid.control.retrieve_slices_by_dbid'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/slices_by_block$', 'catmaid.control.retrieve_slices_by_block'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/set_parent_slices$', 'catmaid.control.set_parent_slice'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/get_parent_slices$', 'catmaid.control.retrieve_parent_slices'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/get_child_slices$', 'catmaid.control.retrieve_child_slices'),

     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/insert_end_segment$', 'catmaid.control.insert_end_segment'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/insert_continuation_segment$', 'catmaid.control.insert_continuation_segment'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/insert_branch_segment$', 'catmaid.control.insert_branch_segment'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/segments_block$', 'catmaid.control.set_segments_block'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/segments_by_hash$', 'catmaid.control.retrieve_segments_by_hash'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/segments_by_id$', 'catmaid.control.retrieve_segments_by_dbid'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/segments_by_block$', 'catmaid.control.retrieve_segments_by_block'),

     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/clear_segments$', 'catmaid.control.clear_segments'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/clear_slices$', 'catmaid.control.clear_slices'),
     (r'^(?P<project_id>\d+)/stack/(?P<stack_id>\d+)/sopnet/clear_blocks$', 'catmaid.control.clear_blocks'),

     )
