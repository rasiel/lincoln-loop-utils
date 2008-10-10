from lincolnloop.upload.models import FileUpload
from django.core.files.base import ContentFile
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.conf import settings
import urllib, urlparse, datetime

def all(request):
    if not request.user.is_staff:
        raise Http404
    files = FileUpload.objects.all().order_by('-upload_date')
    return render_to_response('upload/base.html', {'files': files, 'textarea_id': request.GET['textarea']}, context_instance=RequestContext(request))

def images(request):
    if not request.user.is_staff:
        raise Http404
    files = FileUpload.objects.filter(content_type = 'image').order_by('-upload_date')
    return render_to_response('upload/base.html', {'files': files, 'textarea_id': request.GET['textarea']}, context_instance=RequestContext(request))
    
def files(request):
    if not request.user.is_staff:
        raise Http404
    not_files = ['video', 'image']
    files = FileUpload.objects.exclude(content_type__in = not_files).order_by('-upload_date')
    return render_to_response('upload/base.html', {'files': files, 'textarea_id': request.GET['textarea']}, context_instance=RequestContext(request))
    
def youtube(request):
    if not request.user.is_staff:
        raise Http404
    import elementtree.ElementTree as ET
    try:
        user = settings.YOU_TUBE_USER
        needs_user_setting = False
    except AttributeError:
        user = 'NBC'
        needs_user_setting = True
    gdata_feed = "http://gdata.youtube.com/feeds/videos?author=%s&orderby=updated" % (user,)
    root = ET.parse(urllib.urlopen(gdata_feed)).getroot()
    videos = []
    for e in root.findall('{http://www.w3.org/2005/Atom}entry'):
        video = {}
        video['title'] = e.findtext('{http://www.w3.org/2005/Atom}title')
        date = e.findtext('{http://www.w3.org/2005/Atom}published').split('T')[0]
        video['upload_date'] = date
        media = e.find('{http://search.yahoo.com/mrss/}group')
        video['description'] = media.findtext('{http://search.yahoo.com/mrss/}description')
        video['thumb'] = media.find('{http://search.yahoo.com/mrss/}thumbnail').attrib['url']
        video['image'] = media.findall('{http://search.yahoo.com/mrss/}thumbnail')[-1].attrib['url']
        video['url'] = media.find('{http://search.yahoo.com/mrss/}content').attrib['url']
        videos.append(video)
    return render_to_response('upload/youtube.html', {'videos': videos, 'textarea_id': request.GET['textarea'], 'needs_user_setting': needs_user_setting}, context_instance=RequestContext(request))
    
def flickr(request):
    if not request.user.is_staff:
         raise Http404
    import flickr
    try:
        user = settings.FLICKR_USER
        flickr.API_KEY = settings.FLICKR_API_KEY
    except AttributeError:
        return HttpResponse('You need to set <tt>FLICKR_USER</tt> and <tt>FLICKR_API_KEY</tt> in your settings file. <br />&larr; <a href="/uploads/?textarea=%s">Back to all uploads.</a>' % (request.GET['textarea'],))
    # Get first 12 photos for the user
    flickr_photos = flickr.people_getPublicPhotos(user, 12, 1)
    photos = []
    #this loop is too slow. needs caching or a better library?
    for f in flickr_photos:
        photo = {}
        photo['url'] = f.getURL('Small', 'source')
        photo['link'] = f.getURL()
        photo['title'] = f._Photo__title
        photo['upload_date'] = datetime.datetime.fromtimestamp(float(f._Photo__dateposted))
        photos.append(photo)
    return render_to_response('upload/flickr.html', {'photos': photos, 'textarea_id': request.GET['textarea']}, context_instance=RequestContext(request))
    
def download(request):
    '''Saves image from URL and returns ID for use with AJAX script'''
    if not request.user.is_staff:
        raise Http404
    title = request.GET['title'] or 'untitled'
    description = request.GET['description']
    url = urllib.unquote(request.GET['photo'])
    file_content = urllib.urlopen(url).read()
    upload_file = ContentFile(file_content)
    file_name = url.split('/')[-1]
    f = FileUpload.objects.create(title=title,description=description)
    f.upload.save(file_name, upload_file)
    f.save()
    return HttpResponse('%s' % (f.id))