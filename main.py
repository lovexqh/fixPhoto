#! /usr/bin/python
# coding=utf-8
import struct
import os, shutil


def typeList():
    return {
        "FFD8FF": "JPEG",
        "49492A00080000001C00FE00040001": "NEF",
        "89504E47": "PNG"}


def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


def filetype(filename):
    print filename
    print "\n"
    binfile = open(filename, 'rb')
    tl = typeList()
    ftype = 'unknown'
    for hcode in tl.keys():
        numOfBytes = len(hcode) / 2
        binfile.seek(0)
        hbytes = struct.unpack_from("B" * numOfBytes, binfile.read(numOfBytes))
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = tl[hcode]
            break
    binfile.close()
    return ftype


def mycopyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print "%s not exist!" % (srcfile)
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        print "copy %s -> %s" % (srcfile, dstfile)


if __name__ == '__main__':
    path = r'E:\FOUND.000'
    for parent, dirNames, filenames in os.walk(path):
        for filename in filenames:
            fileSuffix = filetype(parent + "\\" + filename)
            print fileSuffix
            mycopyfile(parent + "\\" + filename, "E:\photo\\" + filename[:-3] + fileSuffix)
