# -*- coding: utf-8 -*-
import argparse




if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("posfile", help=u"输入pos file路径")
    parser.add_argument("logfile", help=u"输入log file路径")
    args = parser.parse_args()
    print args.posfile
    print args.logfile
