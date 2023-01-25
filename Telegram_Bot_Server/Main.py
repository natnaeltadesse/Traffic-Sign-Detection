import numpy as np
import cons as key
import time
import cv2
from PIL import Image
from keras.models import load_model
from telegram import Update
import telegram.ext.filters as F

from telegram.ext import *

classes = {1: 'Speed limit (20km/h)',
           2: 'Speed limit (30km/h)',
           3: 'Speed limit (50km/h)',
           4: 'Speed limit (60km/h)',
           5: 'Speed limit (70km/h)',
           6: 'Speed limit (80km/h)',
           7: 'End of speed limit (80km/h)',
           8: 'Speed limit (100km/h)',
           9: 'Speed limit (120km/h)',
           10: 'No passing',
           11: 'No passing veh over 3.5 tons',
           12: 'Right-of-way at intersection',
           13: 'Priority road',
           14: 'Yield',
           15: 'Stop',
           16: 'No vehicles',
           17: 'Veh > 3.5 tons prohibited',
           18: 'No entry',
           19: 'General caution',
           20: 'Dangerous curve left',
           21: 'Dangerous curve right',
           22: 'Double curve',
           23: 'Bumpy road',
           24: 'Slippery road',
           25: 'Road narrows on the right',
           26: 'Road work',
           27: 'Traffic signals',
           28: 'Pedestrians',
           29: 'Children crossing',
           30: 'Bicycles crossing',
           31: 'Beware of ice/snow',
           32: 'Wild animals crossing',
           33: 'End speed + passing limits',
           34: 'Turn right ahead',
           35: 'Turn left ahead',
           36: 'Ahead only',
           37: 'Go straight or right',
           38: 'Go straight or left',
           39: 'Keep right',
           40: 'Keep left',
           41: 'Roundabout mandatory',
           42: 'End of no passing',
           43: 'End no passing veh > 3.5 tons'}

print("Bot Started...")

model = load_model('traffic_classifier.h5')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    await update.message.reply_text(f'🤖Hey {user.first_name} Send me an image of a traffic sign and I will try to '
                                    f'predict its class.')


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    message_id = update.message.message_id
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")


    image = Image.open('user_photo.jpg')
    image = image.resize((30, 30))


    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    pred = model.predict(image)

    class_index = np.argmax(pred)
    class_name = classes[class_index + 1]

    i = await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"🤖Okay Give Me A Sec, I'm Working On Your FIle🛠️")
    time.sleep(2)

    for k in range(10, 101, 5):
        await i.edit_text(text=f"🤖Please wait...... {k}%")
        time.sleep(0.01)

    if pred[0, class_index] < 0.6:
        await i.edit_text(text="❌❌❌")
        await i.reply_text(reply_to_message_id=message_id,
                           text=f"🤖Sorry, I Couldn't Recognize The Sign☹️...Please Try Again")
    else:
        await i.edit_text(text="✅✅✅")

        acc = pred[0, class_index] * 100
        await i.reply_text(reply_to_message_id=message_id,
                           text=f"🤖I think this is a \"{class_name}\" traffic sign.(%.2f " % acc + "%)")


def main():
    updater = ApplicationBuilder().token(key.API_KEY).build()
    updater.add_handler(CommandHandler('start', start))
    updater.add_handler(MessageHandler(F.PHOTO, photo))
    updater.run_polling()


if __name__ == '__main__':
    main()
