import hmac
import hashlib
import paho.mqtt.client as mqtt
# This is the Subscriber
while True:
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("Seed")
    def on_message(client, userdata, msg):
        global seed
        seed = msg.payload.decode()
        client.disconnect()
        return seed
    client = mqtt.Client()
    client.connect("172.17.37.163",1883,60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
    Network_Prefix='2001:db8:3c4d:15'
    key_str = 'Secret_key'
    key = bytes (key_str , 'utf-8')
    Node_ID = '130'
    Salted_ID_str = Node_ID + seed
    Salted_ID = bytes (Salted_ID_str , 'utf-8')
    digest_maker = hmac.new(key, Salted_ID, hashlib.sha1)
    f = open('hmac_sha.py', 'rb')
    try:
        while True:
            block = f.read(1024)
            if not block:
                break
                digest_maker.update(block)
    finally:
        f.close()
    digest = digest_maker.hexdigest()
    h = hashlib.blake2b(digest_size=8)
    p = bytes (digest, 'utf-8')
    z = h.update(p)
    IPx = h.hexdigest()
    IP =IPx[0:4]+':'+IPx[4:8]+':'+IPx[8:12]+':'+IPx[12:16]
    IPv6=Network_Prefix+':'+IP
    g = hashlib.blake2b(digest_size=6)
    t = bytes (digest, 'utf-8')
    c = g.update(t)
    MACx = g.hexdigest()
    MAC =MACx[0:2]+':'+MACx[2:4]+':'+MACx[4:6]+':'+MACx[6:8]+':'+MACx[8:10]+':'+MACx[10:]

    print('Seed is:',seed)
    # print (IPv6)
    print ('MAC is:',MAC)

    import os
    sudoPassword = 'Mohannad'
    command = 'ls'
    os.system('echo %s|sudo -S ifconfig'%sudoPassword)
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    os.system('echo %s|sudo -S /etc/init.d/networking stop'%sudoPassword)
    os.system('echo %s|sudo -S ifconfig enp0s3 hw ether %s'%(sudoPassword, MAC))
    os.system('echo %s|sudo -S /etc/init.d/networking start'%sudoPassword)
    os.system('echo %s|sudo -S ifconfig'%sudoPassword)

    continue
