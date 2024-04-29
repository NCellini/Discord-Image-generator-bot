import requests
import json
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()  # load all the variables from the .env file
api_key = os.getenv('API_KEY')
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
text2img = 'https://stablediffusionapi.com/api/v3/text2img'
img2img = 'https://stablediffusionapi.com/api/v3/img2img'


def create_image_collage(image_links, path):
    if not os.path.exists(f"./images/{path}"):
        os.makedirs(f"./images/{path}")

    image1 = Image.open(requests.get(image_links[0], stream=True).raw)
    image2 = Image.open(requests.get(image_links[1], stream=True).raw)
    image3 = Image.open(requests.get(image_links[2], stream=True).raw)
    images = [image1, image2, image3]

    if len(image_links) == 4:
        image4 = Image.open(requests.get(image_links[3], stream=True).raw)
        images.append(image4)

    i = 1

    for image in images:
        image.save(f"./images/{path}/img{i}.png")
        i += 1

    if len(image_links) == 4:
        new_image = Image.new('RGB', (1024, 1024), (250, 250, 250))
        new_image.paste(images[0], (0, 0))
        new_image.paste(images[1], (512, 0))
        new_image.paste(images[2], (0, 512))
        new_image.paste(images[3], (512, 512))
        new_image.save(f"./images/{path}/img_collage.png")
    else:
        new_image = Image.new('RGB', (1536, 512), (250, 250, 250))
        new_image.paste(images[0], (0, 0))
        new_image.paste(images[1], (512, 0))
        new_image.paste(images[2], (1024, 0))
        new_image.save(f"./images/{path}/img_collage.png")


def create_text2img_json(prompt):
    return {
        'key': api_key,
        'prompt': prompt,
        'negative_prompt': '((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly '
                           'drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), '
                           '((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), ((bad proportions)), '
                           '((extra limbs)), cloned face, (((skinny))), glitchy, ((extra breasts)), ((double torso)), '
                           '((extra arms)), ((extra hands)), ((mangled fingers)), ((missing breasts)), '
                           '(missing lips), ((ugly face)), ((fat)), ((extra legs))',
        'width': '512',
        'height': '512',
        'samples': '4',
        'num_inference_steps': '20',
        'safety_checker': 'yes',
        'enhance_prompt': 'yes',
        'seed': None,
        'guidance_scale': 7.5,
        'webhook': None,
        'track_id': None
    }


def create_img2img_json(prompt, init_image):
    return {
        "key": api_key,
        "prompt": prompt,
        "negative_prompt": '((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly '
                           'drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), '
                           '((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), ((bad proportions)), '
                           '((extra limbs)), cloned face, (((skinny))), glitchy, ((extra breasts)), ((double torso)), '
                           '((extra arms)), ((extra hands)), ((mangled fingers)), ((missing breasts)), '
                           '(missing lips), ((ugly face)), ((fat)), ((extra legs))',
        "init_image": init_image,
        "width": "512",
        "height": "512",
        "samples": "3",
        "num_inference_steps": "30",
        "safety_checker": "yes",
        "enhance_prompt": "yes",
        "guidance_scale": 7.5,
        "strength": 0.7,
        "seed": None,
        "webhook": None,
        "track_id": None
    }


def text2img_call(prompt):
    info_json = json.dumps(create_text2img_json(prompt))
    response = requests.post(text2img, data=info_json, headers=headers)
    return response.json()


def img2img_call(prompt, img_link):
    info_json = json.dumps(create_img2img_json(prompt, img_link))
    response = requests.post(img2img, data=info_json, headers=headers)
    return response.json()


def create_test_response():
    return {'status': 'success',
            'generationTime': 4.859086990356445,
            'id': 4634511,
            'output': [
                'https://pub-8b49af329fae499aa563997f5d4068a4.r2.dev/generations/f5b4f920-a6f8-42e3-9ca9-56b1a518c342'
                '-0.png',
                'https://pub-8b49af329fae499aa563997f5d4068a4.r2.dev/generations/f5b4f920-a6f8-42e3-9ca9-56b1a518c342'
                '-1.png',
                'https://pub-8b49af329fae499aa563997f5d4068a4.r2.dev/generations/f5b4f920-a6f8-42e3-9ca9-56b1a518c342'
                '-2.png',
                'https://pub-8b49af329fae499aa563997f5d4068a4.r2.dev/generations/f5b4f920-a6f8-42e3-9ca9-56b1a518c342'
                '-3.png'],
            'meta': {'H': 512,
                     'W': 512,
                     'enable_attention_slicing': 'true',
                     'file_prefix': 'f5b4f920-a6f8-42e3-9ca9-56b1a518c342',
                     'guidance_scale': 7.5,
                     'model': 'runwayml/stable-diffusion-v1-5',
                     'n_samples': 4,
                     'negative_prompt': '((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), '
                                        '((poorly drawn face)), (((mutation))), (((deformed))), (((tiling))), '
                                        '((naked)), ((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, '
                                        '((bad anatomy)), ((bad proportions)), ((extra limbs)), cloned face, '
                                        '(((skinny))), glitchy, ((extra breasts)), ((double torso)), ((extra arms)), '
                                        '((extra hands)), ((mangled fingers)), ((missing breasts)), (missing lips), '
                                        '((ugly face)), ((fat)), ((extra legs)), anime ((out of frame)), '
                                        '((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly drawn '
                                        'face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), '
                                        '((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), '
                                        '((bad proportions)), ((extra limbs)), cloned face, glitchy, '
                                        '((extra breasts)), ((double torso)), ((extra arms)), ((extra hands)), '
                                        '((mangled fingers)), ((missing breasts)), (missing lips), ((ugly face)), '
                                        '((fat)), ((extra legs))',
                     'outdir': 'out',
                     'prompt': 'ultra realistic close up portrait ((beautiful pale cyberpunk female with heavy black '
                               'eyeliner)), blue eyes, shaved side haircut, hyper detail, cinematic lighting, '
                               'magic neon, dark red city, Canon EOS R3, nikon, f/1.4, ISO 200, 1/160s, 8K, RAW, '
                               'unedited, symmetrical balance, in-frame, 8K ((ultra realistic eyes)) ((detailed '
                               'face)), DSLR photography, sharp focus, Unreal Engine 5, Octane Render, Redshift, ',
                     'revision': 'fp16',
                     'safetychecker': 'yes',
                     'seed': 1454902171,
                     'steps': 20,
                     'vae': 'stabilityai/sd-vae-ft-mse'}}


def create_img_test_response():
    return {'status': 'success',
            'generationTime': 8.113376379013062,
            'id': 4633085,
            'output': [
                'https://pub-8b49af329fae499aa563997f5d4068a4.r2.dev/generations/9b2708eb-42d2-4391-a28e-74638b12cb44'
                '-0.png'],
            'meta': {'H': 512,
                     'W': 512,
                     'file_prefix': '9b2708eb-42d2-4391-a28e-74638b12cb44',
                     'guidance_scale': 7.5,
                     'init_image': 'https://pub-8b49af329fae499aa563997f5d4068a4.r2.dev/generations/4b50fec2-dc13'
                                   '-4875-8681-8fd5b45344b5-0.png',
                     'n_samples': 1,
                     'negative_prompt': '',
                     'outdir': 'out',
                     'prompt': 'a cat sitting on a bench',
                     'safetychecker': 'yes',
                     'seed': 2462501841,
                     'steps': 20,
                     'strength': 0.7}}

