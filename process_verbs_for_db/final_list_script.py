import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
conjugation_app_dir = os.path.join(current_dir, '..')
sys.path.append(conjugation_app_dir)


from app.conjugate import Conjugador
from extract_verbs_from_pdf import verbs as pdf
from extract_verbs_from_ods import verbs as ods
from time import sleep

verbs_to_add = [
    'usar', 'cerrar', 'construir', 'empeorar', 'arruinar', 'conectar', 'prestar', 'cobrar', 'ofrecer', 'comprar',
    'costar', 'perder', 'encontrar', 'escuchar', 'conocer', 'parecer', 'acordar', 'aprender', 'enseñar', 'nacer',
    'matar', 'arrepentirse', 'gustar', 'interesar', 'cortar', 'enjuagar', 'dibujar', 'aparecer', 'entrar', 'mudar', 'atropellar'
]

combined_list = pdf + ods + verbs_to_add
verbs = sorted(set(combined_list))

final_list_path = os.path.join(current_dir, 'final_list_new.txt')
no_disponibles_path = os.path.join(current_dir, 'verbos_no_disponibles_new.txt')

cnt_norm, cnt_no_disp = 1, 1

with open(final_list_path, 'w', encoding='utf-8') as final_list, \
     open(no_disponibles_path, 'w', encoding='utf-8') as no_disponibles_file:

    for verb in verbs:
        verbse = verb + 'se'
        # print(verbse)
        try:
            if verb != 'embaír':
                conjugator = Conjugador(verbse)
                if not conjugator.infinitivo.endswith('se'):
                    final_list.write(verb + '\n')
                    cnt_norm += 1
                else:
                    final_list.write(verb.lower() + '\n')
                    final_list.write(verbse.lower() + '\n')
                    final_list.flush()
                    cnt_norm += 2
            else:
                no_disponibles_file.write(verb.lower() + '\n')
                no_disponibles_file.flush()
                cnt_no_disp += 1

        except TypeError as e:
            no_disponibles_file.write(verb.lower() + '\n')
            no_disponibles_file.flush()
            cnt_no_disp += 1

        sleep(0.1)

print(f"Final list contain {cnt_norm} words.\n{cnt_no_disp} words weren't found on the reference web site.")
