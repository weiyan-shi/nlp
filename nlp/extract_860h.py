import json
import os

fis = ['/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_310_2021_NONE/ASR_CN_RECORDING_310_11865/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2021_860h/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_310_2021_NONE/nt12_20_tt_train/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_310_2021_NONE/temp/310_recording_test/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_310_2021_NONE/temp/nt1.2/nt12.txt',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_310_2021_NONE/temp/nt2.0/nt2.txt',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_310_2021_NONE/gen_tts_train/gen_tts_part1/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_310_2021_NONE/gen_tts_train/gen_tts_part2/gen_tts.txt',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_310_2021_NONE/310_tts_train/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_310_2021_NONE/310_tts_train2/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_310_2021_NONE/ASR_CN_CHILD_HAITIAN_202112_30271/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2020_1500h/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2021_450h/wavs/sz_individuation_0813_p1_100000/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2021_450h/wavs/zx_individuation_0802_p2_80000/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2021_450h/wavs/sz_individuation_0820_p1_150000/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2021_450h/wavs/sz_individuation_0901_p1_200000/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2021_450h/wavs/zx_individuation_0820_p1_150000/text',
       '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2021_450h/wavs/sz_individuation_0802_p1_80000/text']

fis=[
    '/mnt/beegfs/home/asr/data/feature80/2021_751h/text',
     '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2020_1500h/text',
'/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2021_450h/wavs/sz_individuation_0802_p1_80000/text',
     '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2021_450h/wavs/sz_individuation_0813_p1_100000/text',
     '/mnt/beegfs/home/asr/data/wav/cn/ASR_CN_ADULT_NIO_NONE_2021_450h/wavs/sz_individuation_0820_p1_150000/text',

     ]

with open('wav.scp', 'w') as w_f:
    for fi in fis:
        with open(fi) as f:
            lines = f.readlines()
            for line in lines:
                path, obj = line.split(',', 1)
                dic = json.loads(obj)
                if dic['id'] == 2:
                    p, filename = os.path.split(path)
                    key = filename[:-4]
                    print(key)
                    w_f.write(key + ' ' + path + '\n')
