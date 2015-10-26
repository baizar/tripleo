cat << EOF > /usr/bin/bootif-fix
#!/usr/bin/env bash

while true;
        do find /httpboot/ -type f ! -iname "kernel" ! -iname "ramdisk" ! -iname "*.kernel" ! -iname "*.ramdisk" -exec sed -i 's|{mac|{net0/mac|g' {} +;
done
EOF

chmod a+x /usr/bin/bootif-fix

cat << EOF > /usr/lib/systemd/system/bootif-fix.service
[Unit]
Description=Automated fix for incorrect iPXE BOOFIF

[Service]
Type=simple
ExecStart=/usr/bin/bootif-fix

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable bootif-fix
systemctl start bootif-fix
