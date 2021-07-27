import pytz

timezone = pytz.timezone('Asia/Ho_Chi_Minh')


def localize_datetime(datetime):
    return timezone.localize(datetime)

def get_generated_index(object_class, code_character):
    last_object = (
        object_class.objects.all_with_deleted()
            .order_by('-code').first()
    )
    if not last_object:
        index = 1
    else:
        last_code = last_object.code
        char_length = len(code_character)
        index = int(last_code[char_length:]) + 1
    return index

def get_generated_code(object_class, code_character):
    index = get_generated_index(object_class, code_character)
    generated_code = code_character + str(index).rjust(6, '0')
    return generated_code