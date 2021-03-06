import json
import time

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from djsopnet.models import *

# --- JSON conversion ---
def slice_dict(slice):
    sd = {'id' : slice.id,
          'assembly' : slice.assembly,
          'hash' : slice.hash_value,
          'section' : slice.section,
          'box' : [slice.min_x, slice.min_y, slice.max_x, slice.max_y],
          'ctr' : [slice.ctr_x, slice.ctr_y],
          'value' : slice.value,
          'x' : slice.shape_x,
          'y' : slice.shape_y,
          'parent' : slice.parent.id}
    return sd

def segment_dict(segment):
    sd = {'id' : segment.id,
          'assembly' : segment.assembly,
          'hash' : segment.hash_value,
          'section' : segment.section_inf,
          'box' : [segment.min_x, segment.min_y, segment.max_x, segment.max_y],
          'ctr' : [segment.ctr_x, segment.ctr_y],
          'type' : segment.type,
          'slice_a' : segment.slice_a.id,
          'slice_b' : -1,
          'slice_c' : -1}

    if segment.slice_b:
        sd['slice_b'] = segment.slice_b.id
    if segment.slice_c:
        sd['slice_c'] = segment.slice_c.id

    return sd

def block_dict(block):
    bd = {'id' : block.id,
          'slices' : block.slices_flag,
          'segments' : block.segments_flag,
          'box' : [block.min_x, block.min_y, block.min_z,
                   block.max_x, block.max_y, block.max_z]}
    return bd

def block_info_dict(block_info):
    bid = {'size' : [block_info.height, block_info.width, block_info.depth],
           'count' : [block_info.num_x, block_info.num_y, block_info.num_z]}
    return bid

def generate_slice_response(slice):
    if slice:
        return HttpResponse(json.dumps(slice_dict(slice)), mimetype = 'text/json')
    else:
        return HttpResponse(json.dumps({'id' : -1}), mimetype = 'text/json')

def generate_segment_response(segment):
    if segment:
        return HttpResponse(json.dumps(segment_dict(segment)), mimetype = 'text/json')
    else:
        return HttpResponse(json.dumps({'id' : -1}), mimetype = 'text/json')


def generate_slices_response(slices):
    slice_list = [slice_dict(slice) for slice in slices]
    return HttpResponse(json.dumps({'slices' : slice_list}), mimetype = 'text/json')

def generate_segments_response(segments):
    segment_list = [segment_dict(segment) for segment in segments]
    return HttpResponse(json.dumps({'segments' : segment_list}), mimetype = 'text/json')

def generate_block_response(block):
    if block:
        return HttpResponse(json.dumps(block_dict(block)), mimetype = 'text/json')
    else:
        return HttpResponse(json.dumps({'id' : -1}), mimetype = 'text/json')

def generate_block_info_response(block_info):
    if block_info:
        return HttpResponse(json.dumps(block_info_dict(block_info)), mimetype = 'text/json')
    else:
        return HttpResponse(json.dumps({'id' : -1}), mimetype = 'text/json')

# --- Blocks ---

def setup_blocks(request, dataset_id = None):
    '''
    Initialize and store the blocks and block info in the db, associated with
    the given dataset, if these things don't already exist.
    '''
    try:
        width = int(request.GET.get('width'))
        height = int(request.GET.get('height'))
        depth = int(request.GET.get('depth'))
    except:
        return HttpResponse(json.dumps({'ok' : False}), mimetype='text/json')

    ds = get_object_or_404(Dataset, pk=dataset_id)
    u = User.objects.get(id=1)

    nx = ds.dimension.x / width;
    ny = ds.dimension.y / height;
    nz = ds.dimension.z / depth;

    # If dataset size is not equally divisible by block size...
    if nx * width < ds.dimension.z:
        nx = nx + 1;

    if ny * height < ds.dimension.y:
        ny = ny + 1;

    if nz * depth < ds.dimension.z:
        nz = nz + 1;

    try:
        info = BlockInfo.objects.get(dataset=ds)
        return HttpResponse(json.dumps({'ok': False}), mimetype='text/json')
    except BlockInfo.DoesNotExist:

        info = BlockInfo(user = u, dataset = ds,
                         height = height, width = width, depth = depth,
                         num_x = nx, num_y = ny, num_z = nz)
        info.save();


    for z in range(0, s.dimension.z, depth):
        for y in range(0, s.dimension.y, height):
            for x in range(0, s.dimension.x, width):
                block = Block(user=u, dataset=ds, min_x = x, min_y = y, min_z = z,
                              max_x = x + width, max_y = y + height, max_z = z + depth,
                              slices = [], segments = [], slices_flag = False,
                              segments_flag = False)
                block.save();
    return HttpResponse(json.dumps({'ok': True}), mimetype='text/json')

def block_at_location(request, dataset_id = None):

    s = get_object_or_404(Dataset, pk=dataset_id)
    try:
        x = int(request.GET.get('x'))
        y = int(request.GET.get('y'))
        z = int(request.GET.get('z'))
        # Block are closed-open, thus lte/gt
        block = Block.objects.get(dataset = ds,
                                 min_x__lte = x,
                                 min_y__lte = y,
                                 min_z__lte = z,
                                 max_x__gt = x,
                                 max_y__gt = y,
                                 max_z__gt = z)
        return generate_block_response(block)
    except:
        return generate_block_response(None)


def block_info(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk=dataset_id)
    try:
        block_info = BlockInfo.objects.get(dataset = ds)
        return generate_block_info_response(block_info)
    except:
        return generate_block_info_response(None)

def set_block_slice_flag(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk=dataset_id)
    block_id = int(request.GET.get('block_id'))
    flag = int(request.GET.get('flag'))
    try:
        block = Block.objects.get(dataset = ds, id = block_id)
        block.slices_flag = flag
        block.save()
        return HttpResponse(json.dumps({'ok': True}), mimetype='text/json')
    except:
        HttpResponse(json.dumps({'ok': False}), mimetype='text/json')

def set_block_segment_flag(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk=dataset_id)
    block_id = int(request.GET.get('block_id'))
    flag = int(request.GET.get('flag'))
    try:
        block = Block.objects.get(dataset = ds, id = block_id)
        block.segments_flag = flag
        block.save()
        return HttpResponse(json.dumps({'ok': True}), mimetype='text/json')
    except:
        HttpResponse(json.dumps({'ok': False}), mimetype='text/json')

# --- Slices ---

def insert_slice(request, dataset_id = None):
    ds = get_object_or_404(Dataset, pk = dataset_id)
    u = User.objects.get(id = 1)

    try:
        section = int(request.GET.get('section'))
        hash_value = int(request.GET.get('hash'))
        ctr_x = float(request.GET.get('cx'))
        ctr_y = float(request.GET.get('cy'))
        xstr = request.GET.getlist('x[]')
        ystr = request.GET.getlist('y[]')
        value = float(request.GET.get('value'))
    except:
        return HttpResponse(json.dumps({'id' : -1}), mimetype='text/json')

    print ' '.join(xstr)
    print ' '.join(ystr)

    x = map(int, xstr)
    y = map(int, ystr)

    if x and y:
        min_x = min(x)
        min_y = min(y)
        max_x = max(x)
        max_y = max(y)
    else:
        min_x = -1
        min_y = -1
        max_x = -1
        max_y = -1

    slice = Slice(dataset = ds, user = u,
                  assembly = None, hash_value = hash_value, section = section,
                  min_x = min_x, min_y = min_y, max_x = max_x, max_y = max_y,
                  ctr_x = ctr_x, ctr_y = ctr_y, value = value,
                  shape_x = x, shape_y = y, size = len(x), parent = None)
    slice.save()

    return HttpResponse(json.dumps({'id': slice.id}), mimetype='text/json')


def set_slices_block(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)

    try:
        slice_ids_str = request.GET.getlist('slice[]')
        block_id = int(request.GET.get('block'))

        slice_ids = map(int, slice_ids_str)

        block = Block.objects.get(id = block_id)

        slices = Slice.objects.filter(dataset = ds, id__in = slice_ids)

        ok_slice_ids = [qslice.id for qslice in slices]

        block.slices.extend(ok_slice_ids)

        block.save();

        return HttpResponse(json.dumps({'ok' : True}), mimetype='text/json')

    except Block.DoesNotExist:
        return HttpResponse(json.dumps({'ok' : False}), mimetype='text/json')


def retrieve_slices_by_hash(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)
    hash_values_str = request.GET.getlist('hash[]')
    hash_values = map(int, hash_values_str)
    slices = Slice.object.filter(dataset = ds, hash_value__in = hash_values)
    return generate_slices_response(slices)

def retrieve_slices_by_dbid(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)
    ids_str = request.GET.get('id[]')
    ids = map(int, ids_str)
    slices = Slice.object.filter(dataset = ds, id__in = ids)
    return generate_slices_response(slices)


def retrieve_slices_by_block(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)
    block_id = int(request.GET.get('block_id'))
    try:
        block = Block.objects.get(dataset = ds, id = block_id)
        slice_ids = block.slices
        slices = Slice.object.filter(dataset = ds, id__in = slice_ids)
        return generate_slices_response(slices)
    except:
        return generate_slices_response(Slice.objects.none())

def set_parent_slice(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)
    try:
        child_id_strs = request.GET.getlist('child_id[]')
        parent_id_strs = reqeust.GET.getlist('parent_id[]')

        child_ids = map(int, child_id_strs)
        parent_ids = map(int, parent_id_str)

        # TODO: figure out how to do this in a single db hit.
        for child_id, parent_id in zip(child_ids, parent_ids):
            child = Slice.objects.get(dataset = ds, id = child_id)
            parent = Slice.objects.get(dataset = ds, id = parent_id)
            child.parent = parent
            child.save()
        return HttpResponse(json.dumps({'ok' : True}), mimetype = 'text/json')
    except:
        return HttpResponse(json.dumps({'ok' : False}), mimetype = 'text/json')

def retrieve_parent_slices(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)

    cp_array = []

    try:
        ids_str = request.GET.getlist('id[]')
        ids = map(int, ids_str)
        children = Slice.objects.get(dataset = ds, id__in = ids)
        for child in children:
            cp_array.append({'child' : child.id, 'parent' : child.parent.id})
    except:
        pass

    return HttpResponse(json.dumps({'cp_map' : cp_array}), mimetype = 'text/json')

def retrieve_child_slices(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)
    pc_array = []

    try:
        ids_str = request.GET.getlist('id[]')
        ids = map(int, ids_str)
        parents = Slice.objects.filter(dataset = ds, id__in = ids)

        for parent in parents:
            children = Slice.objects.filter(dataset = ds, parent = parent)
            pc_array.append({'parent' : parent.id,
                             'children' : [child.id for child in children]})
    except:
        pass

    return HttpResponse(json.dumps({'pc_map' : pc_array}), mimetype = 'text/json')

# --- Segments ---

def insert_end_segment(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)

    try:
        hash_value = int(request.GET.get('hash'))
        slice_id = int(request.GET.get('slice_id'))
        direction = int(request.GET.get('direction'))
        ctr_x = float(request.GET.get('cx'))
        ctr_y = float(request.GET.get('cy'))

        slice = Slice.objects.get(dataset = ds, id = slice_id)

        segment = Segment(dataset = ds, assembly = None, hash_value = hash_value,
                          section_inf = slice.section, min_x = slice.min_x,
                          min_y = slice.min_y, max_x = slice.max_x, max_y = slice.max_y,
                          ctr_x = ctr_x, ctr_y = ctr_y, type = 0, direction = direction,
                          slice_a = slice)
        segment.save()
        return HttpResponse(json.dumps({'id': segment.id}), mimetype='text/json')
    except Slice.DoesNotExist:
        return HttpResponse(json.dumps({'id': -1}), mimetype='text/json')




def insert_continuation_segment(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)

    try:
        hash_value = int(request.GET.get('hash'))
        slice_a_id = int(request.GET.get('slice_a_id'))
        slice_b_id = int(request.GET.get('slice_b_id'))
        direction = int(request.GET.get('direction'))
        ctr_x = float(request.GET.get('cx'))
        ctr_y = float(request.GET.get('cy'))

        slice_a = Slice.objects.get(dataset = ds, id = slice_a_id)
        slice_b = Slice.objects.get(dataset = ds, id = slice_b_id)

        min_x = min(slice_a.min_x, slice_b.min_x)
        min_y = min(slice_a.min_y, slice_b.min_y)
        max_x = max(slice_a.max_x, slice_b.max_x)
        max_y = max(slice_a.max_y, slice_b.max_y)
        section = min(slice_a.section, slice_b.section)

        segment = Segment(dataset = ds, assembly = None, hash_value = hash_value,
                          section_inf = section, min_x = min_x,
                          min_y = min_y, max_x = max_x, max_y = max_y,
                          ctr_x = ctr_x, ctr_y = ctr_y, type = 1, direction = direction,
                          slice_a = slice_a, slice_b = slice_b)
        segment.save()
        return HttpResponse(json.dumps({'id': segment.id}), mimetype='text/json')
    except Slice.DoesNotExist:
        return HttpResponse(json.dumps({'id': -1}), mimetype='text/json')


def insert_branch_segment(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)

    try:
        hash_value = int(request.GET.get('hash'))
        slice_a_id = int(request.GET.get('slice_a_id'))
        slice_b_id = int(request.GET.get('slice_b_id'))
        slice_c_id = int(request.GET.get('slice_c_id'))
        direction = int(request.GET.get('direction'))
        ctr_x = float(request.GET.get('cx'))
        ctr_y = float(request.GET.get('cy'))

        slice_a = Slice.objects.get(dataset = ds, id = slice_a_id)
        slice_b = Slice.objects.get(dataset = ds, id = slice_b_id)
        slice_c = Slice.objects.get(dataset = ds, id = slice_c_id)

        min_x = min(min(slice_a.min_x, slice_b.min_x), slice_c.min_x)
        min_y = min(min(slice_a.min_y, slice_b.min_y), slice_c.min_y)
        max_x = max(max(slice_a.max_x, slice_b.max_x), slice_c.max_x)
        max_y = max(max(slice_a.max_y, slice_b.max_y), slice_c.max_y)
        section = min(min(slice_a.section, slice_b.section), slice_c.section)

        segment = Segment(dataset = ds, assembly = None, hash_value = hash_value,
                          section_inf = section, min_x = min_x,
                          min_y = min_y, max_x = max_x, max_y = max_y,
                          ctr_x = ctr_x, ctr_y = ctr_y, type = 1, direction = direction,
                          slice_a = slice_a, slice_b = slice_b, slice_c = slice_c)
        segment.save()
        return HttpResponse(json.dumps({'id': segment.id}), mimetype='text/json')
    except Slice.DoesNotExist:
        return HttpResponse(json.dumps({'id': -1}), mimetype='text/json')
    pass

def set_segments_block(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)

    segment_ids_str = request.GET.getlist('segment[]')
    block_id = int(request.GET.get('block'))

    segment_ids = map(int, segment_id_str)

    try:
        block = Block.objects.get(id = block_id)

        segments = Segment.objects.filter(dataset = ds, id__in = segment_ids)

        ok_segment_ids = [qsegment.id for qsegment in segments]

        block.segments.extend(ok_segment_ids)

        block.save();

        return HttpResponse(json.dumps({'ok' : True}), mimetype='text/json')

    except Block.DoesNotExist:
        return HttpResponse(json.dumps({'ok' : False}), mimetype='text/json')
    pass

def retrieve_segments_by_hash(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)
    hash_values_str = request.GET.getlist('hash[]')
    hash_values = map(int, hash_values_str)
    segments = Segment.object.filter(dataset = ds, hash_value__in = hash_values)
    return generate_segments_response(segments)

def retrieve_segments_by_dbid(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)
    ids_str = request.GET.getlist('id[]')
    ids = map(int, ids_str)
    segments = Segment.object.filter(dataset = ds, id__in = ids)
    return generate_segments_response(segments)

def retrieve_segments_by_block(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)
    block_id = int(request.GET.get('block_id'))
    try:
        block = Block.objects.get(dataset = ds, id = block_id)
        segment_ids = block.segments
        segments = Segment.object.filter(dataset = ds, id__in = segment_ids)
        return generate_segments_response(segments)
    except:
        return generate_segments_response(Segment.objects.none())

# --- convenience code for debug purposes ---
def clear_slices(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)
    sure = request.GET.get('sure')
    if sure == 'yes':
        Slice.object.filter(dataset = ds).delete()
        return HttpResponse(json.dumps({'ok' : True}), mimetype='text/json')
    else:
        HttpResponse(json.dumps({'ok' : False}), mimetype='text/json')

def clear_segments(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)
    sure = request.GET.get('sure')
    if sure == 'yes':
        Segment.object.filter(dataset = ds).delete()
        return HttpResponse(json.dumps({'ok' : True}), mimetype='text/json')
    else:
        HttpResponse(json.dumps({'ok' : False}), mimetype='text/json')

def clear_blocks(request, dataset_id = None):
    s = get_object_or_404(Dataset, pk = dataset_id)
    sure = request.GET.get('sure')
    if sure == 'yes':
        Block.object.filter(dataset = ds).delete()
        BlockInfo.object.filter(dataset = ds).delete()
        return HttpResponse(json.dumps({'ok' : True}), mimetype='text/json')
    else:
        HttpResponse(json.dumps({'ok' : False}), mimetype='text/json')

