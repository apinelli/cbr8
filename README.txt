This script sends specific show commands to CBR8 and RPD for troubleshooting video issues.
Please have the following info available prior to running the script:

- CBR8 ip address
- RPD ip address
- CBR8 username
- CBR8 password
- File name for RPD show commands (make sure it ends with 2 exit commands)
- File name for CBR8 show commands

It will ssh to the RPD through the CBR8 connection and it considers RPD default password.

Script will take more than 15 minutes to complete. It will work along with 2 files (that have
to be copied to the same folder as the python file). The files below were created for the lab CBR8
10.122.151.12 (RTP) and its RPD 14.2.64.221.

- rpd_show_commands.txt
- [VER-2]show_tshoots_cbr8_rtp1.txt

Running this program will yield 2 files:

- cbr8_collection_<ip>_<date> : with the output results for CBR8
- rpd_collection_<ip>_<date> : with the output results for RPD



