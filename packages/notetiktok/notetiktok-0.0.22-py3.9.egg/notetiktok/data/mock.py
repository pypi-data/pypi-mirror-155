from notetiktok.data import add_image_list, add_video, add_video_list
import os

from notesecret import generate_key, read_secret

read_secret(cate1='notetiktok', cate2='dataset', cate3='db_path',
            value=f'sqlite:////home/bingtao/workspace/tmp/data/notetiktok.db')


key = read_secret(cate1='notetiktok', cate2='cipher_key', cate3='source0')
if key is None:
    key = read_secret(cate1='notetiktok', cate2='cipher_key', cate3='source0', value=generate_key())

video_list = [
    'https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/videos/butterfly.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/videos/hls/bee.m3u8',
    'https://flutter.github.io/assets-for-api-docs/assets/videos/hls/bee0.ts',
    'https://flutter.github.io/assets-for-api-docs/assets/videos/hls/bee1.ts',
    'https://flutter.github.io/assets-for-api-docs/assets/videos/hls/bee2.ts',
    'https://flutter.github.io/assets-for-api-docs/assets/widgets/align_transition_plain.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/widgets/animated_align.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/widgets/animated_container.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/widgets/animated_default_text_style.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/widgets/animated_opacity.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/widgets/animated_padding.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/widgets/animated_physical_model.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/widgets/animated_positioned.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/widgets/animated_positioned_directional.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/widgets/animated_theme.mp4',
    'https://flutter.github.io/assets-for-api-docs/assets/widgets/custom_scroll_view.mp4',
]
image_list = [
    "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fdesk-fd.zol-img.com.cn%2Ft_s960x600c5%2Fg5%2FM00%2F02%2F05%2FChMkJ1bKyaOIB1YfAAusnvE99Z8AALIQQPgER4AC6y2052.jpg&refer=http%3A%2F%2Fdesk-fd.zol-img.com.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1653893347&t=e81cdb517382b238ab0add7d593d82f9",
    "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fpic1.win4000.com%2Fwallpaper%2F2018-06-15%2F5b236a18acfc0.jpg&refer=http%3A%2F%2Fpic1.win4000.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1653893347&t=e9803366ccc95d31830d7feff2853949",
    "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fpic1.win4000.com%2Fwallpaper%2Fc%2F54376f06e80b6.jpg%3Fdown&refer=http%3A%2F%2Fpic1.win4000.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1653893347&t=73588f90d5cae45689208109ddd08cff",
    "https://cdn.pixabay.com/photo/2013/07/18/20/26/sea-164989_1280.jpg",
    "https://cdn.pixabay.com/photo/2013/04/04/12/34/mountains-100367_1280.jpg",
    "https://cdn.pixabay.com/photo/2016/10/18/21/22/beach-1751455_1280.jpg",
    "https://cdn.pixabay.com/photo/2014/10/07/13/48/mountain-477832_1280.jpg",
    "https://cdn.pixabay.com/photo/2018/08/14/13/23/ocean-3605547_1280.jpg",
    "https://pics3.baidu.com/feed/55e736d12f2eb93882bb23a9f5d85b3ce7dd6fde.jpeg?token=5b5ea1fce5330981604afde51aea480a",
    "https://pics2.baidu.com/feed/0823dd54564e925828741d2083380f51cebf4e84.jpeg?token=ddf4482cde6507bdf9ce35c2fa8e6b17",
    "https://pics3.baidu.com/feed/2cf5e0fe9925bc318fe4ea3a556553b8ca13701f.jpeg?token=d6a150ad89ea32bbc033c36dd2ed40ce",
    "https://pics5.baidu.com/feed/64380cd7912397dd1df3692e54386cbed1a28752.jpeg?token=685b038dbb77257809e1dd2370bfa2a8",
    "https://pics3.baidu.com/feed/9f2f070828381f303dede237a7bb92016c06f0f8.jpeg?token=0bb182fc4076563cf45900573aac2799",
    "https://pics0.baidu.com/feed/7e3e6709c93d70cf72ba0f6ef0660f09bba12b50.jpeg?token=b796708bb8c5a392fafbe6f3a45607f6",
    "https://pics6.baidu.com/feed/3801213fb80e7bec51de4b24309467319a506b36.jpeg?token=a7053681906f31fe1c21f9ff25594001", ]

add_image_list(image_list)
add_video_list(video_list)

print(key)
add_video(
    url='https://flutter.github.io/assets-for-api-docs/assets/widgets/custom_scroll_view.mp4',
    title='别看了，这是加密的',
    cipher_key=key
)
