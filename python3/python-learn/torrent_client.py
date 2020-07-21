import xmlrpclib
import libtorrent as lt
import random
import time


server = xmlrpclib.ServerProxy('http://127.0.0.1:1989')



def fetch_torrent(ses, info_hash):
    print '+' * 60
    info_hash = info_hash.upper()
    url = 'magnet:?xt=urn:btih:%s' % (info_hash,)
    print "url:", url
    params = {
        'save_path': 'downloads',
        'storage_mode': lt.storage_mode_t(2),
        'paused': False,
        'auto_managed': False,
        'duplicate_is_error': True
    }
    handle = lt.add_magnet_uri(ses, url, params)
    status = ses.status()
    handle.set_sequential_download(1)
    down_time = time.time()
    if handle.has_metadata():
        info = handle.get_torrent_info()
        print '\n', time.ctime(), (time.time()-down_time), 's, got', url, info.name()
        print 'status', 'p', status.num_peers, 'g', status.dht_global_nodes, 'ts', status.dht_torrents, 'u', status.total_upload, 'd', status.total_download
        meta = info.metadata()
        print meta
        return meta
    else:
        print "no metadata"
    ses.remove_torrent(handle)
    print '+' * 60, '\n'




if __name__ == '__main__':
    r = random.randrange(10000, 50000)
    ses = lt.session()
    ses.listen_on(r, r+10)
    ses.add_dht_router('router.bittorrent.com',6881)
    ses.add_dht_router('router.utorrent.com',6881)
    ses.add_dht_router('dht.transmission.com',6881)
    ses.add_dht_router('70.39.87.34',6881)
    ses.start_dht()

    while True:
        info_hash = server.get_hash().upper()
        fetch_torrent(ses, info_hash)
