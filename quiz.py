from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb9fwIwe09q2aCD6oNqsasPsYYYysBlpyDLjxSjGuOiGi2RbnVq69keO8THsXq8pLClD6jA0vWIAW1keDDEE46xrBPNX9V3vW0VSOfCFzDfXAlVsRTe0SBTAtajE_hi-SNFq02vs0yK_floPDg1CilClDaT0RJUN6JSrY5y5EgJ5MxXx8='

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
