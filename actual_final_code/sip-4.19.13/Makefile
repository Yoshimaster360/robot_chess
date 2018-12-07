
all:
	@(cd sipgen; $(MAKE))
	@(cd siplib; $(MAKE))

install:
	@(cd sipgen; $(MAKE) install)
	@(cd siplib; $(MAKE) install)
	@test -d $(DESTDIR)/usr/lib/python3/dist-packages || mkdir -p $(DESTDIR)/usr/lib/python3/dist-packages
	cp -f sipconfig.py $(DESTDIR)/usr/lib/python3/dist-packages/sipconfig.py
	cp -f /home/cc/ee106a/fa18/class/ee106a-abh/ros_workspaces/lab5/src/ik/launch/lab5/robot_chess/actual_final_code/sip-4.19.13/sipdistutils.py $(DESTDIR)/usr/lib/python3/dist-packages/sipdistutils.py
	/usr/bin/python3 /home/cc/ee106a/fa18/class/ee106a-abh/ros_workspaces/lab5/src/ik/launch/lab5/robot_chess/actual_final_code/sip-4.19.13/mk_distinfo.py "$(DESTDIR)" /usr/lib/python3/dist-packages/sip-4.19.13.dist-info installed.txt

clean:
	@(cd sipgen; $(MAKE) clean)
	@(cd siplib; $(MAKE) clean)
