from django.conf.urls import patterns, url

from djsopnet import views

# Sopnet API
urlpatterns += patterns('',
     (r'^dataset/(?P<dataset_id>\d+)/setup_blocks$', 'djsopnet.setup_blocks'),
     (r'^dataset/(?P<dataset_id>\d+)/block_at_location$', 'djsopnet.block_at_location'),
     (r'^dataset/(?P<dataset_id>\d+)/block$', 'djsopnet.block_info'),

     (r'^dataset/(?P<dataset_id>\d+)/segment_flag$', 'djsopnet.set_block_segment_flag'),
     (r'^dataset/(?P<dataset_id>\d+)/slice_flag$', 'djsopnet.set_block_slice_flag'),
     (r'^dataset/(?P<dataset_id>\d+)/insert_slice$', 'djsopnet.insert_slice'),
     (r'^dataset/(?P<dataset_id>\d+)/slices_block$', 'djsopnet.set_slices_block'),
     (r'^dataset/(?P<dataset_id>\d+)/slices_by_hash$', 'djsopnet.retrieve_slices_by_hash'),
     (r'^dataset/(?P<dataset_id>\d+)/slices_by_id$', 'djsopnet.retrieve_slices_by_dbid'),
     (r'^dataset/(?P<dataset_id>\d+)/slices_by_block$', 'djsopnet.retrieve_slices_by_block'),
     (r'^dataset/(?P<dataset_id>\d+)/set_parent_slices$', 'djsopnet.set_parent_slice'),
     (r'^dataset/(?P<dataset_id>\d+)/get_parent_slices$', 'djsopnet.retrieve_parent_slices'),
     (r'^dataset/(?P<dataset_id>\d+)/get_child_slices$', 'djsopnet.retrieve_child_slices'),

     (r'^dataset/(?P<dataset_id>\d+)/insert_end_segment$', 'djsopnet.insert_end_segment'),
     (r'^dataset/(?P<dataset_id>\d+)/insert_continuation_segment$', 'djsopnet.insert_continuation_segment'),
     (r'^dataset/(?P<dataset_id>\d+)/insert_branch_segment$', 'djsopnet.insert_branch_segment'),
     (r'^dataset/(?P<dataset_id>\d+)/segments_block$', 'djsopnet.set_segments_block'),
     (r'^dataset/(?P<dataset_id>\d+)/segments_by_hash$', 'djsopnet.retrieve_segments_by_hash'),
     (r'^dataset/(?P<dataset_id>\d+)/segments_by_id$', 'djsopnet.retrieve_segments_by_dbid'),
     (r'^dataset/(?P<dataset_id>\d+)/segments_by_block$', 'djsopnet.retrieve_segments_by_block'),

     (r'^dataset/(?P<dataset_id>\d+)/clear_segments$', 'djsopnet.clear_segments'),
     (r'^dataset/(?P<dataset_id>\d+)/clear_slices$', 'djsopnet.clear_slices'),
     (r'^dataset/(?P<dataset_id>\d+)/clear_blocks$', 'djsopnet.clear_blocks'),
)
