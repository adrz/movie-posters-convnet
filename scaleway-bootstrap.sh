v=$(scw images --no-trunc=true | grep image-movieposters)
imageid=$(echo $v | awk '{print $3}')

# for i in {1..3}; do
#     scw create --name="www-$i" --ip-address=none $imageid
# done

for i in {10..13}; do
    scw create --name="www-$i" --ip-address=none --commercial-type=VC1S $imageid
done


sleep 30
for i in {10..13}; do
    scw start www-$i
    sleep 1
done


scw create --commercial-type=VC1S --name haproxy ubuntu-xenial
sleep 30
scw start haproxy

while ! [ $(scw ps|grep haproxy|awk '{ print $6 }') = "running" ]; do
    sleep 20
    scw start haproxy
done


# for i in {1..3};
# do
#     state=$(scw ps|grep "www-$i"|awk '{ print $6 }')
#     while ! [ "$state" = "running" ]
#     do
# 	sleep 20
# 	scw start www-$i
# 	state=$(scw ps|grep "www-$i"|awk '{ print $6 }')
#     done
# done

scw exec haproxy 'apt-get update && apt-get install -q -y haproxy' < /dev/null &
sleep 10


cp haproxy.cfg haproxy_boot.cfg
for i in {1..3}; do
    privateip=$(scw exec --gateway=haproxy www-$i ifconfig eth0 | grep "inet addr" | cut -d ':' -f 2 | cut -d ' ' -f 1)
    echo "	server web$i.local  $privateip:80">> haproxy_boot.cfg
done

cat haproxy_boot.cfg | scw exec haproxy 'cat > /etc/haproxy/haproxy.cfg'
sleep 10
scw exec haproxy 'sudo service haproxy restart'
