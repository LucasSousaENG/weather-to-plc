- Thanks for the attention. The following instructions are necessary for the understanding and running of the code.
Requirements:
1 - Python snap7 (utilizes python 3 32 bits, search for the correct install instructions)
2 - pprint
3 - requests (we get the info from an API on https://www.visualcrossing.com/)
4 - time
5 - Pillow (only if you want to show images while running the code)

*The "Image.open" sector is not obligatory and you need to set up the image you want to substitute.

*extractweatherdata() request a weather API to get all the information. For it to work, you need to create an account and set your ideal configuration for the information you need.

*currentconditions are gathered as a dictionary, each condition are set as a key. Use pprint to better view it's content.

*writePLC sends the conditions for the PLC, in bytes, by connecting to its IP, RACK and SLOT and setting it's DB_NUMBER, START_ADRESS and SIZE.


Some configurations may cause confusion for being in portuguese language, if needed, I can translate and change most part of the code to help you understand. If that is the case, send me an email or comment :).