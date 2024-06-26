#!/usr/bin/env python

import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    exit()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQA)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_ERR:
        MIFAREReader = MFRC522.MFRC522()
        
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        
        Sector = 8

        # Print UID
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, Sector, key, uid)
        print("\n")

        # Check if authenticated
        if status == MIFAREReader.MI_OK:

            # Variable for the data to write
            data = []

            # Fill the data with 0xFF
            for x in range(0,16):
                data.append(0xFF)

            print("Sector Sector looked like this:")
            # Read block Sector
            MIFAREReader.MFRC522_Read(Sector)
            print("\n")

            print("Sector Sector will now be filled with 0xFF:")
            # Write the data
            MIFAREReader.MFRC522_Write(Sector, data)
            print("\n")

            print("It now looks like this:")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(Sector)
            print("\n")

            data = b"___my data :)___"

            # Fill the data with 0x00

            
            print("Now we fill it with 0x00:")
            MIFAREReader.MFRC522_Write(Sector, data)
            print("\n")

            print("It is now empty:")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(Sector)
            print("\n")

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()

            # Make sure to stop reading for cards
            continue_reading = False
        else:
            print("Authentication error")
