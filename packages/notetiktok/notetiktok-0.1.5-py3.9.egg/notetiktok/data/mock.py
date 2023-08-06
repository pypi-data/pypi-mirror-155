from notesecret import generate_key, read_secret
from notetiktok.data import add_video

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

for video in video_list:
    add_video(
        url=video,
        title='this is mock'
    )

print(key)
add_video(
    url='https://flutter.github.io/assets-for-api-docs/assets/widgets/custom_scroll_view.mp4',
    title='别看了，这是加密的',
    cipher_key=key
)
