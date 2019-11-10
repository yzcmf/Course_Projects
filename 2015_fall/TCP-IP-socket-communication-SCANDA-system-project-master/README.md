Read me:

1.Read the final report part 1 and has a basic understanding of the SCADA we are going to build

2.Read the final report part 2 and learn has this idea be realized based on the embedded system.

3.Login in one board, run the RTU_KERNEL file program in the kernel module

4. Login in the same board, run the PROJECT_RTU_USER file program in the user space, use the command “ifconfigure” to get the IP of the board. And run it by use the  “./project_RTU_user+space+IP+space+port_number”. The port number is greater than 2000.For example, “./project_RTU_user 10.3.52.16 2200”.

5. Login in the other board, run the PROJECT_GENERAL_USER file program in the user space. And run it by using the command “./project_GENERAL_user+space+port_number”. The port number is greater than 2000. For example, “./project_ GENERAL _user 2200”.

6. Be careful to the space, the upper case and the lower case, you should use the same with the name of your file in the Linux program.

7. The buttons are connected to the DIO in the TS-7250 board that is used as the testing board as well. 

8.You need a sin wave generate circuit and the output connects to the MAX 197 (chip in the TS-7250 board) corresponding bits.




My email is yzcmf@mail.missouri.edu; If you want the part 1 and part 2 report to learn more, just send me an email, I'll get in touch with you as soon as possible.