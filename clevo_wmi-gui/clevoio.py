import os

def readfile(f):
    with open(f, "rb") as fi:
        return fi.read().decode("UTF-8").strip()


def writefile(f, val):
    print("Writing " + str(val) + " to " + str(f))

    #TODO
    cmd = "echo " + val +  " > " + f
    print(os.popen(cmd).read())

    #fails silently with "w"
    #fi = os.fdopen(os.open(f, os.O_WRONLY | os.O_APPEND | os.O_EXCL), "w")
    #print(fi.write(val))

    #[Errno 22] Invalid argument
    #with open(f, "w+b", buffering=0) as fi:
    #with open(f, "w") as fi:
    #    try:
    #        #fi.write(bytes(val, "ASCII"))
    #    except Exception as e:
    #        print("Error while writing: ", e)