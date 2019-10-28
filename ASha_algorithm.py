import hmac
import hashlib
import random
import time
Network_Prefix='2001:db8:3c4d:15'
key_str = 'Secret_key'
key = bytes (key_str , 'utf-8')
seed_str = []
for i in range(0, 8):
    e = str(int(random.randrange(128,255)))
    seed_str.append(e)
#print('Seeds are: ', seed_str)
#Node_ID = ['130', '170', '195', '215']
Node_ID = []
for x in range(128,256):
    Node_ID.append(str(x))
for i in seed_str:
    #seed =  bytes (seed_str[i] , 'utf-8')
    #print('Key is: ',key)
    #print('Seed is: ',key)
    Salted_ID = []
    digest_maker = []
    digest = []
    IPv6 = []
    MAC = []
    counter = 0
    for j in Node_ID:
        Salted_ID_str = j + i
        l =  bytes (Salted_ID_str , 'utf-8')
        Salted_ID.append(l)
        n = hmac.new(key, Salted_ID[counter], hashlib.sha1)
        digest_maker.append(n)
        f = open('hmac_sha.py', 'rb')
        try:
            while True:
                block = f.read(1024)
                if not block:
                    break
                digest_maker[counter].update(block)
        finally:
            f.close()
        o = digest_maker[counter].hexdigest()
        digest.append(o)
        #print ('Sha1 digest is: ',digest[counter])
        h = hashlib.blake2b(digest_size=8)
        p =  bytes (digest[counter] , 'utf-8')
        z = h.update(p)
        IPx = h.hexdigest()
        #print(IPx)
        IP =IPx[0:4]+':'+IPx[4:8]+':'+IPx[8:12]+':'+IPx[12:16]
        g=Network_Prefix+':'+IP
        IPv6.append(g)
        #print('IP is: ',IPv6)
        g = hashlib.blake2b(digest_size=6)
        t =  bytes (digest[counter] , 'utf-8')
        c = g.update(t)
        MACx = g.hexdigest()
        #print(MACx)
        M =MACx[0:2]+':'+MACx[2:4]+':'+MACx[4:6]+':'+MACx[6:8]+':'+MACx[8:10]+':'+MACx[10:]
        MAC.append(M)
        #print('MAC is: ',MAC)
        counter = counter + 1
    if len(IPv6) > len(set(IPv6)) or len(MAC) > len(set(MAC)):
        print("Fail!")
        continue
    # print (Salted_ID)
    # print (digest)
    #print (IPv6)
    #print (MAC)
    print(i)
    #publish seed using mqtt
    import paho.mqtt.client as mqtt
    client = mqtt.Client()
    client.connect("localhost",1883,60)
    client.publish("Seed", i)
    client.disconnect()
    tiempo = time.time()
    while time.time() < tiempo+60:
        pass
    continue
