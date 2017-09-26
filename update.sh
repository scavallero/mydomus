service mydomus stop
cp -r html /usr/local/mydomus
cp -r plugins /usr/local/mydomus
cp -r sensors /usr/local/mydomus
cp *.py /usr/local/mydomus
service mydomus start

