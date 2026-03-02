from tkinter import *           # Interface gráfica
from tkinter.font import Font   # Fontes
from PIL import ImageTk, Image  # Manipulação de Imagens
import time

# Global variables
active_area = 1                 # Área ativa (1-6) - qual rádio está selecionado
current_level = 0               # Nível de interface (0-off, 1-main freq, 2-advance, 4-teste, 5-não desenvolvida)
current_radio = 1               # Rádio selecionado
current_page = 1                # Página atual
pressed_side_btn = 0            #
transponder_indicator = 0
zeroise_value = False           # Estado especial 1
emergency_value = False         # Estado especial 2
start_time = None
timer = None
boot_screen_active = False      # Controla se a tela de boot está ativa
boot_start_time = None          # Armazena quando a tela de boot foi mostrada

# Manual constants
# Dimensões da tela
x_screen = 206
y_screen = 130
screen_width = 250
screen_height = 290 
padx_screen = 2
pady_screen = 4
padx_area = 1
pady_area = 1

# Automatic constants
full_area_width = screen_width - 2 * padx_screen
main_area_width = (screen_width - 2 * padx_screen - 2 * padx_area) / 2
main_area_height = (screen_height - 2 * pady_screen - 6 * pady_area) * 10 / 37
test_big_box_height = (screen_height - 2 * pady_screen) * 2 / 13
test_small_box_height = (screen_height - 2 * pady_screen) / 13

# Function to help programming and debugging
def log():
    global active_area, current_level, current_radio, current_page, pressed_side_btn
    print("-------")
    print("active_area", active_area)
    print("current_level", current_level)
    print("current_radio", current_radio)
    print("current_page", current_page)
    print("pressed_side_btn", pressed_side_btn)
    print("transponder_indicator", transponder_indicator)

# Reset all variables to default values
def set_default():
    uhf_active.set("399.97")
    uhf_preset.set("399.97")
    hf_active.set("2.000")
    hf_preset.set("2.000")
    atc_active.set("STBY")
    atc_preset.set("6000")
    vhf_active.set("136.975")
    vhf_preset.set("136.975")
    vor_active.set("108.00")
    vor_preset.set("108.00")
    adf_active.set("190.0")
    adf_preset.set("190.0")

# Set all variables to emergency values
def set_emergency_values():
    uhf_active.set("399.97")
    uhf_preset.set("399.97")
    hf_active.set("2.000")
    hf_preset.set("2.000")
    atc_active.set("7700")
    atc_preset.set("EMER")
    vhf_active.set("136.975")
    vhf_preset.set("136.975")
    vor_active.set("108.00")
    vor_preset.set("108.00")
    adf_active.set("190.0")
    adf_preset.set("190.0")

# Function to handle the screen in case the zeroise pin is set
def zeroise():
    global zeroise_value
    zeroise_value = not zeroise_value
    
    if zeroise_value:
        # Reset all variables to default values
        set_default()
    else:
        uhf_preset.set(uhf_active.get())
        hf_preset.set(hf_active.get())
        atc_preset.set("7230")
        vhf_preset.set(vhf_active.get())
        vor_preset.set(vor_active.get())
        adf_preset.set(adf_active.get())

    update_pino_button_image(zeroise_value, zeroise_button)

# Function to handle the screen in case the emergency pin is set
def emergency():
    global emergency_value
    emergency_value = not emergency_value

    if emergency_value:
        uhf_active.set("243.00")
        uhf_preset.set("EMER")
        hf_active.set("2.182")
        hf_preset.set("EMER")
        main_area_3.turn_label_on(main_area_3.stby_label)  # Turn label on in case it was off
        atc_active.set("7700")
        atc_preset.set("EMER")
        vhf_active.set("121.500")
        vhf_preset.set("EMER")
    else:
        uhf_preset.set(uhf_active.get())
        hf_preset.set(hf_active.get())
        atc_active.set("STBY")
        main_area_3.turn_label_on(main_area_3.stby_label)  # Turn label on in case it was off
        atc_preset.set("7231")
        vhf_preset.set(vhf_active.get())

    update_pino_button_image(emergency_value, emergency_button)

# Handles the change of background images of pino btn
def update_pino_button_image(value, button):
    button.update_image(pino_right_img) if value else button.update_image(pino_left_img)

# Function to remove all pages of the screen
# Used before placing a page into the screen to avoid overplacement
def forget_all_pages():
    off_screen.place_forget()
    main_page.place_forget()
    advanced_page.place_forget()
    test_page.place_forget()
    temporary_page.place_forget()
    if 'boot_screen' in globals():
        boot_screen.place_forget()

# Function to show the temporary page while that page has not been developed yet
def show_page_not_developed():
    global active_area

    print("This page does not exist yet")
    forget_all_pages()
    active_area = 1
    temporary_page.place(x=x_screen, y=y_screen)

# Function to show the page that indicates that this screen has not been developed yet
def show_test_page():
    forget_all_pages()
    test_page.place(x=x_screen, y=y_screen)

# Remove indicador de dígito do transponder
def forget_transponder_indicators():
    transponder_canva_1.place_forget()
    transponder_canva_2.place_forget()
    transponder_canva_3.place_forget()
    transponder_canva_4.place_forget()

def get_transponder_indicator():
    global transponder_indicator

    if transponder_indicator == 0:
        forget_transponder_indicators()
        return
    
    if transponder_indicator == 1:
        forget_transponder_indicators()
        transponder_canva_1.place(x=241, y=360)
    elif transponder_indicator == 2:
        forget_transponder_indicators()
        transponder_canva_2.place(x=256, y=360)
    elif transponder_indicator == 3:
        forget_transponder_indicators()
        transponder_canva_3.place(x=269, y=360)
    elif transponder_indicator == 4:
        forget_transponder_indicators()
        transponder_canva_4.place(x=283, y=360)

# Function to clear the page indicator image
def forget_page_icon():
    widget_page_1_2.place_forget()
    widget_page_2_2.place_forget()
    widget_page_1_3.place_forget()
    widget_page_2_3.place_forget()
    widget_page_3_3.place_forget()
    widget_page_1_4.place_forget()
    widget_page_2_4.place_forget()
    widget_page_3_4.place_forget()
    widget_page_4_4.place_forget()

# Function to place a new page indicator image
def place_page_icon(widget):
    forget_page_icon()
    widget.place(x=420, y=370)

# Function to update the image indicator of the page
def update_page_icon():
    global current_level, current_radio, current_page

    if current_level in {0, 4, 5}:
        forget_page_icon()
        forget_transponder_indicators()
        return
    
    if current_level == 1:
        if current_page == 1:
            place_page_icon(widget_page_1_2)
        elif current_page == 2:
            place_page_icon(widget_page_2_2)
    elif current_level == 2:
        if current_radio in {1, 2}:
            if current_page == 1:
                place_page_icon(widget_page_1_3)
            elif current_page == 2:
                place_page_icon(widget_page_2_3)
            elif current_page == 3:
                place_page_icon(widget_page_3_3)

# Function to update the content of the screen
def update_screen():
    global active_area, current_level, current_radio, current_page
    print(f"Global: {active_area}, {current_level}, {current_radio}, {current_page}")
    
    if current_level not in {0, 1, 2, 3, 4, 5}:
        print(f"Erro ao mudar de nível. Current_level = {current_level}")
        return
    
    if current_level == 0:
        print("Turning off")
        forget_all_pages()
        update_page_icon()
        off_screen.place(x=x_screen, y=y_screen)
        return
    
    if current_level == 5:
        update_page_icon()
        show_page_not_developed()
        return
    
    if current_level == 1:
        print("Showing initial screen")
        forget_all_pages()
        update_page_icon()
        main_page.place(x=x_screen, y=y_screen)
        activate_main(1)
        return
    
    if current_level == 2:
        print("Showing advanced screen")
        forget_all_pages()
        update_page_icon()
        advanced_page.place(x=x_screen, y=y_screen)
        activate_advanced(1)

def check_boot_complete():
    """Verifica se os 10 segundos de boot já passaram"""
    global current_level, boot_screen_active, boot_start_time
    
    if not boot_screen_active:
        return
    
    elapsed = time.time() - boot_start_time
    
    # Atualiza a barra de progresso
    boot_screen.update_progress(int(elapsed))
    
    if elapsed >= 10:  # 10 segundos passaram
        # Terminou o boot
        boot_screen_active = False
        current_level = 1
        boot_screen.place_forget()
        update_screen()
    else:
        # Ainda não terminou, verifica novamente em 100ms
        root.after(100, check_boot_complete)

def turn_on_off():
    global current_level, boot_screen_active, boot_start_time

    print("current level", current_level)
    
    if current_level == 0:  # Estava desligado, vai ligar
        # Mostra tela de boot primeiro
        forget_all_pages()
        boot_screen.place(x=x_screen, y=y_screen)
        boot_screen_active = True
        boot_start_time = time.time()  # Marca quando começou
        
        # Muda o ícone do botão
        brt_button.update_image(on_btn_img)
        
        # Agenda a transição para a tela principal
        check_boot_complete()
        
    else:  # Estava ligado, vai desligar
        current_level = 0
        boot_screen_active = False
        brt_button.update_image(off_btn_img)
        update_screen()

# Change the value of the standby frequency of the active area
def change_frequency(is_outer_knob, is_increment):
    global active_area, zeroise_value, emergency_value, transponder_indicator

    areas = [main_area_1, main_area_2, main_area_3, main_area_4, main_area_5, main_area_6]

    if zeroise_value:
        return

    # Determine which variable to use based on the current active area
    if active_area == 1 and not emergency_value:
        delta = 1 if is_outer_knob else 0.25
        stby_var = uhf_preset
        decimals = 2
        min_freq = 225.00
        max_freq = 399.75
    elif active_area == 2 and not emergency_value:
        delta = 0.1 if is_outer_knob else 0.001
        stby_var = hf_preset
        decimals = 3
        min_freq = 2.000
        max_freq = 29.000
    elif active_area == 3 and atc_active.get() == "STBY" and not emergency_value:
        if is_outer_knob:
            if is_increment:
                transponder_indicator += 1
                if transponder_indicator > 4:
                    transponder_indicator = 1
                get_transponder_indicator()
            else:
                transponder_indicator -= 1
                if transponder_indicator < 1:
                    transponder_indicator = 4
                get_transponder_indicator()
        else:
            stby_var = atc_preset
            current_value = int(stby_var.get())

            if transponder_indicator == 1:
                current_value = current_value + 1000 if is_increment else current_value - 1000
            elif transponder_indicator == 2:
                current_value = current_value + 100 if is_increment else current_value - 100
            elif transponder_indicator == 3:
                current_value = current_value + 10 if is_increment else current_value - 10
            elif transponder_indicator == 4:
                current_value = current_value + 1 if is_increment else current_value - 1
            
            current_value = current_value % 8000
            formatted_value = f"{current_value:04d}"
            stby_var.set(formatted_value)
            areas[active_area - 1].update_labels()
        return
    elif active_area == 4 and not emergency_value:
        delta = 1 if is_outer_knob else 0.25
        stby_var = vhf_preset
        decimals = 3
        min_freq = 118.000
        max_freq = 152.000
    elif active_area == 5:
        delta = 1 if is_outer_knob else 0.25
        stby_var = vor_preset
        decimals = 2
        min_freq = 108.00
        max_freq = 118.00
    elif active_area == 6:
        delta = 1 if is_outer_knob else 0.25
        stby_var = adf_preset
        decimals = 1
        min_freq = 100.0
        max_freq = 400.0
    else:
        return

    current_value = float(stby_var.get())
    new_value = current_value + delta if is_increment else current_value - delta

    if new_value > max_freq:
        new_value = min_freq
    elif new_value < min_freq:
        new_value = max_freq

    formatted_value = f"{new_value:.{decimals}f}"
    stby_var.set(formatted_value)
    areas[active_area - 1].update_labels()

# Remove the cyan border of all areas
def deactivate_main_areas():
    areas = [main_area_1, main_area_2, main_area_3, main_area_4, main_area_5, main_area_6]
    for area in areas:
        area.config(bg="gray")
        area.update_labels()

# Set the border to cyan of the given area
def activate_main(main_area_number):
    global active_area, transponder_indicator

    areas = [main_area_1, main_area_2, main_area_3, main_area_4, main_area_5, main_area_6]

    transponder_indicator = 0
    get_transponder_indicator()
    deactivate_main_areas()

    if main_area_number < 1 or main_area_number > len(areas):
        return

    selected_area = areas[main_area_number - 1]
    selected_area.config(bg="cyan")
    active_area = main_area_number

    if active_area == 3:
        transponder_indicator = 1
        get_transponder_indicator()

def deactivate_advanced_areas():
    areas = [advanced_area_1, advanced_area_2, advanced_area_3, advanced_area_4, advanced_area_5, advanced_area_6]
    for area in areas:
        area.config(bg="gray")
        area.update_labels()

def activate_advanced(advanced_area_number):
    global active_area

    areas = [advanced_area_1, advanced_area_2, advanced_area_3, advanced_area_4, advanced_area_5, advanced_area_6]
    deactivate_advanced_areas()

    if advanced_area_number < 1 or advanced_area_number > len(areas):
        return

    selected_area = areas[advanced_area_number - 1]
    selected_area.config(bg="cyan")
    active_area = advanced_area_number

def clear_advanced_variables():
    var_advanced_active.set("")
    var_advanced_preset.set("")
    var_advanced_hf_title.set("")
    var_advanced_hf_selected.set("")
    var_advanced_hf_option0.set("")
    var_advanced_hf_option1.set("")
    var_advanced_hf_option2.set("")
    var_advanced_hf_option3.set("")
    var_advanced_atc_title.set("")
    var_advanced_atc_selected.set("")
    var_advanced_atc_option0.set("")
    var_advanced_atc_option1.set("")
    var_advanced_atc_option2.set("")
    var_advanced_atc_option3.set("")
    var_advanced_vhf_title.set("")
    var_advanced_vhf_selected.set("")
    var_advanced_vhf_option0.set("")
    var_advanced_vhf_option1.set("")
    var_advanced_vhf_option2.set("")
    var_advanced_vhf_option3.set("")
    var_advanced_vor_title.set("")
    var_advanced_vor_selected.set("")
    var_advanced_vor_option0.set("")
    var_advanced_vor_option1.set("")
    var_advanced_vor_option2.set("")
    var_advanced_vor_option3.set("")
    var_advanced_adf_title.set("")
    var_advanced_adf_selected.set("")
    var_advanced_adf_option0.set("")
    var_advanced_adf_option1.set("")
    var_advanced_adf_option2.set("")
    var_advanced_adf_option3.set("")

def get_advanced_variables():
    global current_level, current_radio, current_page
    global uhf_sql_arrow_position
    
    if current_level != 2:
        print("Error: Current level is not 2. Cannot access advanced variables.")
        return
    
    if current_radio == 1 and current_page == 1:
        clear_advanced_variables()
        var_advanced_active.set(uhf_active.get())
        var_advanced_preset.set(uhf_preset.get())
        var_advanced_hf_title.set(uhf_sql_title.get())
        var_advanced_hf_selected.set(uhf_sql_selected.get())
        var_advanced_atc_title.set(uhf_mode_title.get())
        var_advanced_atc_selected.set(uhf_mode_selected.get())
        var_advanced_atc_option0.set(uhf_mode_option0.get())
        var_advanced_atc_option1.set(uhf_mode_option1.get())
        var_advanced_atc_option2.set(uhf_mode_option2.get())
        var_advanced_atc_option3.set(uhf_mode_option3.get())
        var_advanced_vhf_title.set(uhf_aj_title.get())
        var_advanced_vhf_selected.set(uhf_aj_selected.get())
        var_advanced_vor_title.set(uhf_mod_title.get())
        var_advanced_vor_selected.set(uhf_mod_selected.get())
        var_advanced_vor_option0.set(uhf_mod_option0.get())
        var_advanced_vor_option1.set(uhf_mod_option1.get())
        var_advanced_adf_title.set(uhf_mar_title.get())
        var_advanced_adf_selected.set(uhf_mar_selected.get())
        var_advanced_adf_option0.set(uhf_mar_option0.get())
        var_advanced_adf_option1.set(uhf_mar_option1.get())
        var_advanced_adf_option2.set(uhf_mar_option2.get())
        uhf_sql_arrow_position = 3
    elif current_radio == 1 and current_page == 2:
        clear_advanced_variables()
        var_advanced_active.set(uhf_active.get())
        var_advanced_preset.set(uhf_preset.get())
        var_advanced_hf_title.set(uhf_comsec_title.get())
        var_advanced_hf_selected.set(uhf_comsec_selected.get())
        var_advanced_atc_title.set(uhf_aj_title.get())
        var_advanced_atc_selected.set(uhf_aj_selected.get())
        var_advanced_vhf_title.set(uhf_ckey_title.get())
        var_advanced_vhf_selected.set(uhf_ckey_selected.get())
        var_advanced_vor_title.set(uhf_net_title.get())
        var_advanced_vor_selected.set(uhf_net_selected.get())
    elif current_radio == 1 and current_page == 3:
        clear_advanced_variables()
        var_advanced_active.set(uhf_active.get())
        var_advanced_preset.set(uhf_preset.get())
        var_advanced_atc_title.set(uhf_ch_title.get())
        var_advanced_vor_title.set(uhf_test_title.get())
        var_advanced_adf_title.set(uhf_off_title.get())
        var_advanced_adf_selected.set(uhf_off_selected.get())
    elif current_radio == 2 and current_page == 1:
        clear_advanced_variables()
        var_advanced_active.set(hf_active.get())
        var_advanced_preset.set(hf_preset.get())
        var_advanced_hf_title.set(hf_sql_title.get())
        var_advanced_hf_selected.set(hf_sql_selected.get())
        var_advanced_atc_title.set(hf_oper_title.get())
        var_advanced_atc_selected.set(hf_oper_selected.get())
        var_advanced_atc_option0.set(hf_oper_option0.get())
        var_advanced_atc_option1.set(hf_oper_option1.get())
        var_advanced_atc_option2.set(hf_oper_option2.get())
        var_advanced_vhf_title.set(hf_mod_title.get())
        var_advanced_vhf_selected.set(hf_mod_selected.get())
        var_advanced_vhf_option0.set(hf_mod_option0.get())
        var_advanced_vhf_option1.set(hf_mod_option1.get())
        var_advanced_vhf_option2.set(hf_mod_option2.get())
        var_advanced_vhf_option3.set(hf_mod_option3.get())
        var_advanced_vor_title.set(hf_pwr_title.get())
        var_advanced_vor_selected.set(hf_pwr_selected.get())
        var_advanced_adf_title.set(hf_ch_title.get())
    elif current_radio == 2 and current_page == 2:
        clear_advanced_variables()
        var_advanced_active.set(hf_active.get())
        var_advanced_preset.set(hf_preset.get())
        var_advanced_hf_title.set(hf_selcal_title.get())
        var_advanced_hf_selected.set(hf_selcal_selected.get())
        var_advanced_atc_title.set(hf_time_title.get())
        var_advanced_atc_selected.set(hf_time_selected.get())
        var_advanced_vhf_title.set(hf_tx_title.get())
        var_advanced_vhf_selected.set(hf_tx_selected.get())
        var_advanced_vor_title.set(hf_rx_title.get())
        var_advanced_vor_selected.set(hf_rx_selected.get())
        var_advanced_adf_title.set(hf_ch_title.get())
    elif current_radio == 2 and current_page == 3:
        clear_advanced_variables()
        var_advanced_active.set(hf_active.get())
        var_advanced_preset.set(hf_preset.get())
        var_advanced_hf_title.set(hf_ale_title.get())
        var_advanced_hf_selected.set(hf_ale_selected.get())
        var_advanced_hf_option0.set(hf_ale_option0.get())
        var_advanced_hf_option1.set(hf_ale_option1.get())
        var_advanced_hf_option2.set(hf_ale_option2.get())
        var_advanced_hf_option3.set(hf_ale_option3.get())
        var_advanced_atc_title.set(hf_call_title.get())
        var_advanced_atc_selected.set(hf_call_selected.get())
        var_advanced_vhf_title.set(hf_adr_title.get())
        var_advanced_vhf_selected.set(hf_adr_selected.get())
        var_advanced_vor_title.set(hf_freq_title.get())
        var_advanced_vor_selected.set(hf_freq_selected.get())
        var_advanced_adf_title.set(hf_lp_title.get())
        var_advanced_adf_selected.set(hf_lp_selected.get())
    elif current_radio == 4 and current_page == 1:
        clear_advanced_variables()
        var_advanced_active.set(vhf_active.get())
        var_advanced_preset.set(vhf_preset.get())
        var_advanced_hf_title.set(vhf_sql_title.get())
        var_advanced_hf_selected.set(vhf_sql_selected.get())
        var_advanced_vhf_title.set(vhf_off_title.get())
        var_advanced_vhf_selected.set(vhf_off_selected.get())
        var_advanced_vor_title.set(vhf_test_title.get())
        var_advanced_adf_title.set(vhf_ch_title.get())
    else:
        var_advanced_active.set("Temporary Active")
        var_advanced_preset.set("Temporary Preset")

    update_screen()

def key_up3_push():
    global current_level, zeroise_value, emergency_value, current_radio, current_page

    if current_level not in {0, 1, 2, 3, 4, 5}:
        print(f"Erro ao mudar de página. Current_level = {current_level}")
        return
    
    if zeroise_value or emergency_value:
        return
    
    if current_level != 2:
        print("NÃO TEM PRÓXIMA PÁGINA PARA ACESSAR")
        return

    if current_radio == 1:
        current_page = 2 if current_page == 1 else 3 if current_page == 2 else 1
    elif current_radio == 2:
        current_page = 2 if current_page == 1 else 3 if current_page == 2 else 1

    get_advanced_variables()

def key_up4_push():
    global current_level, zeroise_value, emergency_value, current_page, current_radio, active_area

    if zeroise_value or emergency_value:
        return
    
    if current_level not in {0, 1, 2, 3, 4, 5}:
        print(f"Erro ao mudar de nível. Current_level = {current_level}")
        return

    if current_level == 1:
        if active_area not in {1, 2, 4}:
            current_level = 5
            update_screen()
            return
        
        current_radio = active_area
        current_level = 2
        current_page = 1
        get_advanced_variables()
    else:
        current_page = 1
        current_level = 1
        update_screen()

def switch_active_and_preset(active_vars, stby_vars, idx):
    current_value = active_vars[idx].get()
    standby_value = stby_vars[idx].get()
    active_vars[idx].set(standby_value)
    stby_vars[idx].set(current_value)

def toggle_area(side_key_number):
    global active_area, emergency_value, zeroise_value
    global uhf_active, uhf_preset, hf_active, hf_preset, atc_active, atc_preset
    global vhf_active, vhf_preset, vor_active, vor_preset, adf_active, adf_preset

    active_vars = [uhf_active, hf_active, atc_active, vhf_active, vor_active, adf_active]
    stby_vars = [uhf_preset, hf_preset, atc_preset, vhf_preset, vor_preset, adf_preset]

    if active_area < 1 or active_area > 6 or zeroise_value:
        return
    
    if emergency_value:
        if side_key_number == 0:
            if active_area in {1, 2, 3, 4}:
                return
            idx = active_area - 1
            switch_active_and_preset(active_vars, stby_vars, idx)
            return
        elif side_key_number in {1, 2, 3, 4}:
            active_area = side_key_number
            activate_main(active_area)
            return
        else:
            if active_area == side_key_number:
                idx = active_area - 1
                switch_active_and_preset(active_vars, stby_vars, idx)
                return
            active_area = side_key_number
            activate_main(active_area)
            return
    
    if side_key_number != 0 and side_key_number != active_area:
        active_area = side_key_number
        activate_main(active_area)
        return
 
    if active_area == 3:
        if atc_active.get() == "STBY":
            atc_active.set(atc_preset.get())
            main_area_3.turn_label_off(main_area_3.stby_label)
            forget_transponder_indicators()
        else:
            atc_preset.set(atc_active.get())
            main_area_3.turn_label_on(main_area_3.stby_label)
            atc_active.set("STBY")
            get_transponder_indicator()
    else:
        idx = active_area - 1
        switch_active_and_preset(active_vars, stby_vars, idx)

def get_next_option(current_value, options):
    for option in options:
        if option.get() != "" and option.get() != current_value:
            return option.get()
    return current_value

def configure_area(side_key_number):
    global active_area, emergency_value, zeroise_value

    if active_area < 1 or active_area > 6:
        return

    if zeroise_value or emergency_value:
        return
      
    if side_key_number != 0 and side_key_number != active_area:
        active_area = side_key_number
        return
    
    if active_area == 2:
        pass

def side_key_push(side_key_number):
    print(f'Clique esquerdo, botão {side_key_number}')
    global current_level, current_page, pressed_side_btn, active_area, transponder_indicator
    
    print(f"current_level: {current_level}, current_page: {current_page}, pressed_side_btn: {pressed_side_btn}, active_area: {active_area}, transponder_indicator: {transponder_indicator}")

    if pressed_side_btn != 0:
        if pressed_side_btn == 3 and side_key_number == 6:
            transponder_indicator = 0
            forget_transponder_indicators()
            current_level = 4
            show_test_page()
        pressed_side_btn = 0
        unpress_side_buttons()
        return

    if current_level == 1 and current_page == 1:
        toggle_area(side_key_number)
    elif current_level == 2:
        configure_area(side_key_number)
    else:
        print("Erro de páginas do sistema")

def atc_btn_push():
    global active_area, emergency_value, zeroise_value

    if emergency_value or zeroise_value:
        return

    toggle_area(3)

def unpress_side_buttons():
    global pressed_side_btn
    skl_1.update_image(primary_btn_img)
    skl_2.update_image(primary_btn_img)
    skl_3.update_image(primary_btn_img)
    skr_1.update_image(primary_btn_img)
    skr_2.update_image(primary_btn_img)
    skr_3.update_image(primary_btn_img)

def keep_pressing_side_btn(side_key_number, button):
    global pressed_side_btn

    if pressed_side_btn == side_key_number:
        pressed_side_btn = 0
        unpress_side_buttons()
        return

    unpress_side_buttons()
    pressed_side_btn = side_key_number
    button.update_image(primary_btn_pressed_img)
    print("side_key_number", pressed_side_btn)

# Classes
class Btn:
    def __init__(self, root, image, x, y, command=None, right_click_command=None):
        self.button = Button(
            root,
            image=image,
            padx=10,
            pady=5,
            borderwidth=0,
            background="#707070",
            activebackground="#707070",
        )
        self.button.place(x=x, y=y)
        self.button.bind("<Button-1>", self.left_click)
        self.button.bind("<Button-2>", self.right_click)
        self.button.bind("<Button-3>", self.right_click)

        self.command = command
        self.right_click_command = right_click_command

    def left_click(self, event):
        if self.command:
            self.command()

    def right_click(self, event):
        if self.right_click_command:
            self.right_click_command()

    def update_image(self, image):
        self.button.config(image=image)

class Black_btn:
    def __init__(self, root, image, x, y, command=None):
        self.button = Button(
            root,
            command=command,
            image=image,
            padx=10,
            pady=5,
            borderwidth=0,
            background="#000000",
            activebackground="#000000",
        )
        self.button.place(x=x, y=y)

    def update_image(self, image):
        self.button.config(image=image)


class Main_box(Frame):
    def __init__(self, root, active, stby, bg):
        # Definindo as constantes primeiro
        padx_area = 0
        pady_area = 0
        main_area_width = 400
        main_area_height = 200
        active_font = ("Arial", 12)
        stby_font = ("Arial", 10)
        
        super().__init__(root, padx=padx_area, pady=pady_area, bg=bg, 
                        width=main_area_width, height=main_area_height)
        
        self.grid_propagate(False)
        
        # Configuração da matriz 2x3
        for col in range(3):
            self.grid_columnconfigure(col, weight=1)
        for row in range(2):
            self.grid_rowconfigure(row, weight=1)
        
        # Área 1: (1x1 e 2x1) - Coluna 0 inteira
        self.area1 = Frame(self, bg=bg)
        self.area1.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.area1.grid_columnconfigure(0, weight=1)
        self.area1.grid_rowconfigure(0, weight=1)
        self.area1.grid_rowconfigure(1, weight=1)
        
        # Labels da Área 1
        self.active_label1 = Label(
            self.area1,
            textvariable=active,  # "120.15"
            font=active_font,
            background="black",
            fg="cyan",
            anchor='center'
        )
        self.stby_label1 = Label(
            self.area1,
            textvariable=stby,  # "118.15 PT"
            font=stby_font,
            background="black",
            fg="white",
            anchor='center'
        )
        self.active_label1.grid(row=0, column=0, sticky='nsew')
        self.stby_label1.grid(row=1, column=0, sticky='nsew')
        
        # Área 2: (1x2) - Linha 0, Coluna 1
        self.area2 = Frame(self, bg=bg)
        self.area2.grid(row=0, column=1, sticky='nsew')
        self.area2.grid_columnconfigure(0, weight=1)
        self.area2.grid_rowconfigure(0, weight=1)
        
        self.active_label2 = Label(
            self.area2,
            text="---",  # Placeholder
            font=active_font,
            background="black",
            fg="cyan",
            anchor='center'
        )
        self.active_label2.grid(row=0, column=0, sticky='nsew')
        
        # Área 3: (2x2) - Linha 1, Coluna 1
        self.area3 = Frame(self, bg=bg)
        self.area3.grid(row=1, column=1, sticky='nsew')
        self.area3.grid_columnconfigure(0, weight=1)
        self.area3.grid_rowconfigure(0, weight=1)
        
        self.stby_label2 = Label(
            self.area3,
            text="---",  # Placeholder
            font=stby_font,
            background="black",
            fg="white",
            anchor='center'
        )
        self.stby_label2.grid(row=0, column=0, sticky='nsew')
        
        # Área 4: (1x3 e 2x3) - Coluna 2 inteira
        self.area4 = Frame(self, bg=bg)
        self.area4.grid(row=0, column=2, rowspan=2, sticky='nsew')
        self.area4.grid_columnconfigure(0, weight=1)
        self.area4.grid_rowconfigure(0, weight=1)
        self.area4.grid_rowconfigure(1, weight=1)
        
        self.active_label3 = Label(
            self.area4,
            text="---",  # Placeholder
            font=active_font,
            background="black",
            fg="cyan",
            anchor='center'
        )
        self.stby_label3 = Label(
            self.area4,
            text="---",  # Placeholder
            font=stby_font,
            background="black",
            fg="white",
            anchor='center'
        )
        self.active_label3.grid(row=0, column=0, sticky='nsew')
        self.stby_label3.grid(row=1, column=0, sticky='nsew')
        
        # Posiciona o Main_box no grid pai
        self.grid(sticky='nsew')
    
    def turn_label_off(self, label):
        """Esconde o label definindo a cor do texto como preta"""
        label.config(fg="black")
    
    def turn_label_on(self, label):
        """Mostra o label com sua cor apropriada"""
        if label in [self.active_label1, self.active_label2, self.active_label3]:
            label.config(fg="cyan")
        elif label in [self.stby_label1, self.stby_label2, self.stby_label3]:
            label.config(fg="white")
    
    def update_labels(self):
        """Força a atualização dos labels"""
        self.active_label1.update()
        self.active_label2.update()
        self.active_label3.update()
        self.stby_label1.update()
        self.stby_label2.update()
        self.stby_label3.update()


class Test_big_box(Frame):
    def __init__(self, root, title, left_text="", right_text=""):
        super().__init__(root, width=full_area_width, height=test_big_box_height, bg="black")
        self.grid_propagate(False)

        self.title = title
        self.left_text = left_text
        self.right_text = right_text

        self.title_label = Label(
            self,
            textvariable=self.title,
            font=stby_font,
            background="black",
            fg="white"
        )
        self.left_text_label = Label(
            self,
            textvariable=self.left_text,
            font=stby_font,
            background="black",
            fg="white"
        )
        self.right_text_label = Label(
            self,
            textvariable=self.right_text,
            font=stby_font,
            background="black",
            fg="white"
        )
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)
        self.title_label.grid(row=0, column=1, sticky='nswe')
        self.left_text_label.grid(row=0, column=0, sticky='nswe')
        self.right_text_label.grid(row=0, column=2, sticky='nswe')

class Test_small_box(Frame):
    def __init__(self, root, title, description=""):
        super().__init__(root, width=full_area_width, height=test_small_box_height, bg="black")
        self.grid_propagate(False)

        self.title = title
        self.description = description

        self.title_label = Label(
            self,
            textvariable=self.title,
            font=test_body_font,
            background="black",
            fg="white"
        )
        self.description_label = Label(
            self,
            textvariable=self.description,
            font=test_body_font,
            background="black",
            fg="orange"
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.title_label.grid(row=0, column=0, sticky='nswe')
        self.description_label.grid(row=0, column=1, sticky='wns')

class Advanced_sub_box_title(Frame):
    def __init__(self, root, title, subtitle, side):
        super().__init__(root, height=main_area_height, bg="black")
        self.grid_propagate(False)
        sticky_option = 'nse' if side == "right" else 'nsw'
        self.title = Label(
            self,
            textvariable=title,
            font=stby_font,
            background="black",
            fg="white"
        )
        self.subtitle = Label(
            self,
            textvariable=subtitle,
            font=stby_font,
            background="black",
            fg="cyan"
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.title.grid(row=0, column=0, sticky=sticky_option)
        self.subtitle.grid(row=1, column=0, sticky=sticky_option)

class Advanced_sub_box_arrow(Frame):
    def __init__(self, root, side, arrow_position):
        super().__init__(root, height=main_area_height, bg="black")
        self.grid_propagate(False)
        self.arrow_labels = []
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

class Advanced_sub_box_body(Frame):
    def __init__(self, root, side, option0, option1, option2, option3):
        super().__init__(root, height=main_area_height, bg="black")
        self.grid_propagate(False)
        sticky_option = 'nsw' if side == "right" else 'nse'

        self.option0 = Label(self, textvariable=option0, font=option_font, background="black", fg="white")
        self.option1 = Label(self, textvariable=option1, font=option_font, background="black", fg="white")
        self.option2 = Label(self, textvariable=option2, font=option_font, background="black", fg="white")
        self.option3 = Label(self, textvariable=option3, font=option_font, background="black", fg="white")
        
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.option0.grid(row=0, column=0, sticky=sticky_option)
        self.option1.grid(row=1, column=0, sticky=sticky_option)
        self.option2.grid(row=2, column=0, sticky=sticky_option)
        self.option3.grid(row=3, column=0, sticky=sticky_option)

class Advanced_box(Frame):
    def __init__(self, root, bg, left_weight, middle_weight, right_weight):
        super().__init__(root, padx=padx_area, pady=pady_area, bg=bg, width=main_area_width, height=main_area_height)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=left_weight)
        self.grid_columnconfigure(1, weight=middle_weight)
        self.grid_columnconfigure(2, weight=right_weight)
        self.grid_rowconfigure(0, weight=1)
        self.grid(sticky='nsew')

    def update_labels(self):
        pass

class BootScreen(Frame):
    def __init__(self, root):
        super().__init__(root, width=screen_width, height=screen_height, bg="black")
        self.grid_propagate(False)
        
        # Texto principal
        self.title_label = Label(
            self,
            text="RMS SIMULATOR",
            font=Font(family='Miriam Mono CLM', size=16, weight='bold'),
            background="black",
            fg="cyan"
        )
        
        # Texto de inicialização
        self.boot_label = Label(
            self,
            text="INITIALIZING SYSTEMS...",
            font=Font(family='Miriam Mono CLM', size=12),
            background="black",
            fg="white"
        )
        
        # Versão
        self.version_label = Label(
            self,
            text="v1.0.0",
            font=Font(family='Miriam Mono CLM', size=10),
            background="black",
            fg="gray"
        )
        
        # Barra de progresso
        self.progress_label = Label(
            self,
            text="[          ] 0%",
            font=Font(family='Miriam Mono CLM', size=10),
            background="black",
            fg="green"
        )
        
        # Mensagem genérica de teste
        self.test_label = Label(
            self,
            text="SISTEMA INICIADO - TESTE OK",
            font=Font(family='Miriam Mono CLM', size=10),
            background="black",
            fg="yellow"
        )
        
        # Timer countdown
        self.timer_label = Label(
            self,
            text="Iniciando em 10s...",
            font=Font(family='Miriam Mono CLM', size=10),
            background="black",
            fg="orange"
        )
        
        self.position_elements()
    
    def position_elements(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title_label.grid(row=1, column=0, sticky='nsew')
        self.boot_label.grid(row=2, column=0, sticky='nsew')
        self.progress_label.grid(row=3, column=0, sticky='nsew')
        self.test_label.grid(row=4, column=0, sticky='nsew')
        self.timer_label.grid(row=5, column=0, sticky='nsew')
        self.version_label.grid(row=6, column=0, sticky='sew')
    
    def update_progress(self, elapsed_seconds):
        total_seconds = 10
        progress = min(elapsed_seconds / total_seconds, 1.0)
        percentage = int(progress * 100)
        
        bars = int(progress * 10)
        progress_bar = "[" + "=" * bars + " " * (10 - bars) + "]"
        
        if percentage < 30:
            msg = "CARREGANDO SISTEMAS..."
        elif percentage < 60:
            msg = "INICIALIZANDO RÁDIOS..."
        elif percentage < 90:
            msg = "VERIFICANDO FREQUÊNCIAS..."
        else:
            msg = "PRONTO PARA USO"
        
        self.boot_label.config(text=msg)
        self.progress_label.config(text=f"{progress_bar} {percentage}%")
        
        remaining = total_seconds - elapsed_seconds
        if remaining > 0:
            self.timer_label.config(text=f"Iniciando em {remaining}s...")
        else:
            self.timer_label.config(text="INICIANDO...")

# Criação da janela principal
root = Tk()
root.title("Simulador RMS")
root.resizable(False, False)

# Define fonts
active_font = Font(family='Miriam Mono CLM', size=18)
stby_font = Font(family='Miriam Mono CLM', size=16)
option_font = Font(family='Miriam Mono CLM', size=8)
arrow_font = Font(family='Miriam Mono CLM', size=12)
test_body_font = Font(family='Miriam Mono CLM', size=10)

# Load image
try:
    rms_image = ImageTk.PhotoImage(Image.open("Fundo_completo_10.png"))
    rms_label = Label(root, image=rms_image)
    rms_label.pack()
except:
    print("Imagem de fundo não encontrada. Continuando sem fundo.")
    root.configure(bg='black')

# Define button images
try:
    primary_btn_img = PhotoImage(file="bt_normal.png")
    primary_btn_pressed_img = PhotoImage(file="bt_ativo.png")
    atc_btn_img = PhotoImage(file="bt_atc.png")
    ch_btn_img = PhotoImage(file="bt_ch.png")
    idt_btn_img = PhotoImage(file="bt_idt.png")
    pge_btn_img = PhotoImage(file="bt_pge.png")
    seta_btn_img = PhotoImage(file="bt_quadrado_riscado.png")
    key_up4_btn_img = PhotoImage(file="bt_in_out.png")
    triangulo_02_btn_img = PhotoImage(file="bt_tri.png")
    triangulo_01_btn_img = PhotoImage(file="bt_tri.png")
    freq_img = PhotoImage(file="bt_freq2.png")
    on_btn_img = PhotoImage(file="bt_btc_on.png")
    off_btn_img = PhotoImage(file="bt_btc_off.png")
    pino_left_img = PhotoImage(file="toggle_esq.png")
    pino_right_img = PhotoImage(file="toggle.png")
    plus = PhotoImage(file="seta_horario.png")
    minus = PhotoImage(file="seta_antihorario.png")
    page_1_2 = PhotoImage(file="page_1_2.png")
    page_2_2 = PhotoImage(file="page_2_2.png")
    page_1_3 = PhotoImage(file="page_1_3.png")
    page_2_3 = PhotoImage(file="page_2_3.png")
    page_3_3 = PhotoImage(file="page_3_3.png")
    page_1_4 = PhotoImage(file="page_1_4.png")
    page_2_4 = PhotoImage(file="page_2_4.png")
    page_3_4 = PhotoImage(file="page_3_4.png")
    page_4_4 = PhotoImage(file="page_4_4.png")
except:
    print("Algumas imagens não foram encontradas. Verifique os arquivos.")
    # Criar imagens placeholder se necessário
    primary_btn_img = None

# Widgets de página
widget_page_1_2 = Label(root, image=page_1_2 if 'page_1_2' in dir() else None, background="#000000")
widget_page_2_2 = Label(root, image=page_2_2 if 'page_2_2' in dir() else None, background="#000000")
widget_page_1_3 = Label(root, image=page_1_3 if 'page_1_3' in dir() else None, background="#000000")
widget_page_2_3 = Label(root, image=page_2_3 if 'page_2_3' in dir() else None, background="#000000")
widget_page_3_3 = Label(root, image=page_3_3 if 'page_3_3' in dir() else None, background="#000000")
widget_page_1_4 = Label(root, image=page_1_4 if 'page_1_4' in dir() else None, background="#000000")
widget_page_2_4 = Label(root, image=page_2_4 if 'page_2_4' in dir() else None, background="#000000")
widget_page_3_4 = Label(root, image=page_3_4 if 'page_3_4' in dir() else None, background="#000000")
widget_page_4_4 = Label(root, image=page_4_4 if 'page_4_4' in dir() else None, background="#000000")

# Create Pages
main_page = Frame(root, width=screen_width, height=screen_height, pady=pady_screen, bg="black")
off_screen = Frame(root, width=screen_width, height=screen_height, pady=pady_screen, bg="black")
advanced_page = Frame(root, width=screen_width, height=screen_height, pady=pady_screen, bg="black")
test_page = Frame(root, width=screen_width, height=screen_height, pady=pady_screen, bg="black")
temporary_page = Frame(root, width=screen_width, height=screen_height, pady=pady_screen, bg="black")

# Define variables
var_advanced_active = StringVar(value="")
var_advanced_preset = StringVar(value="")
var_advanced_hf_title = StringVar(value="")
var_advanced_hf_selected = StringVar(value="")
var_advanced_hf_option0 = StringVar(value="")
var_advanced_hf_option1 = StringVar(value="")
var_advanced_hf_option2 = StringVar(value="")
var_advanced_hf_option3 = StringVar(value="")
var_advanced_atc_title = StringVar(value="")
var_advanced_atc_selected = StringVar(value="")
var_advanced_atc_option0 = StringVar(value="")
var_advanced_atc_option1 = StringVar(value="")
var_advanced_atc_option2 = StringVar(value="")
var_advanced_atc_option3 = StringVar(value="")
var_advanced_vhf_title = StringVar(value="")
var_advanced_vhf_selected = StringVar(value="")
var_advanced_vhf_option0 = StringVar(value="")
var_advanced_vhf_option1 = StringVar(value="")
var_advanced_vhf_option2 = StringVar(value="")
var_advanced_vhf_option3 = StringVar(value="")
var_advanced_vor_title = StringVar(value="")
var_advanced_vor_selected = StringVar(value="")
var_advanced_vor_option0 = StringVar(value="")
var_advanced_vor_option1 = StringVar(value="")
var_advanced_vor_option2 = StringVar(value="")
var_advanced_vor_option3 = StringVar(value="")
var_advanced_adf_title = StringVar(value="")
var_advanced_adf_selected = StringVar(value="")
var_advanced_adf_option0 = StringVar(value="")
var_advanced_adf_option1 = StringVar(value="")
var_advanced_adf_option2 = StringVar(value="")
var_advanced_adf_option3 = StringVar(value="")

uhf_active = StringVar(value="399.97")
uhf_preset = StringVar(value="299.97")
hf_active = StringVar(value="2.000")
hf_preset = StringVar(value="3.000")
atc_active = StringVar(value="STBY")
atc_preset = StringVar(value="7000")
vhf_active = StringVar(value="136.975")
vhf_preset = StringVar(value="119.975")
vor_active = StringVar(value="108.00")
vor_preset = StringVar(value="168.00")
adf_active = StringVar(value="190.0")
adf_preset = StringVar(value="180.0")

uhf_sql_arrow_position = IntVar(value=0)
uhf_mode_position = IntVar(value=0)
uhf_aj_arrow_position = IntVar(value=0)
uhf_mod_arrow_position = IntVar(value=0)
ufh_mar_arrow_position = IntVar(value=0)

uhf_sql_title = StringVar(value="SQL")
uhf_sql_selected = StringVar(value="OFF")
uhf_mode_title = StringVar(value="MODE")
uhf_mode_selected = StringVar(value="T/R")
uhf_mode_option0 = StringVar(value="T/R")
uhf_mode_option1 = StringVar(value="TR+G")
uhf_mode_option2 = StringVar(value="243")
uhf_mode_option3 = StringVar(value="121")
uhf_aj_title = StringVar(value="AJ")
uhf_aj_selected = StringVar(value="OFF")
uhf_aj_arrow_value = IntVar(value=1)
uhf_mod_title = StringVar(value="MOD")
uhf_mod_selected = StringVar(value="AM")
uhf_mod_option0 = StringVar(value="AM")
uhf_mod_option1 = StringVar(value="OFF")
uhf_mar_title = StringVar(value="MAR")
uhf_mar_selected = StringVar(value="OFF")
uhf_mar_option0 = StringVar(value="OFF")
uhf_mar_option1 = StringVar(value="CST")
uhf_mar_option2 = StringVar(value="SHIP")

uhf_comsec_title = StringVar(value="CSEC")
uhf_comsec_selected = StringVar(value="PT")
uhf_ckey_title = StringVar(value="CKEY")
uhf_ckey_selected = StringVar(value="01")
uhf_net_title = StringVar(value="NET NB")
uhf_net_selected = StringVar(value="---")

uhf_ch_title = StringVar(value="CH")
uhf_test_title = StringVar(value="TEST")
uhf_off_title = StringVar(value="OFF")
uhf_off_selected = StringVar(value="8.33")

hf_sql_title = StringVar(value="SQL")
hf_sql_selected = StringVar(value="LOW")
hf_oper_title = StringVar(value="OPER")
hf_oper_selected = StringVar(value="MAN")
hf_oper_option0 = StringVar(value="MAN")
hf_oper_option1 = StringVar(value="ITU")
hf_oper_option2 = StringVar(value="EMER")
hf_mod_title = StringVar(value="MOD")
hf_mod_selected = StringVar(value="USB")
hf_mod_option0 = StringVar(value="USB")
hf_mod_option1 = StringVar(value="LSB")
hf_mod_option2 = StringVar(value="AM")
hf_mod_option3 = StringVar(value="CW")
hf_pwr_title = StringVar(value="PWR")
hf_pwr_selected = StringVar(value="LOW")
hf_ch_title = StringVar(value="CH")

hf_selcal_title = StringVar(value="SELCAL")
hf_selcal_selected = StringVar(value="OFF")
hf_time_title = StringVar(value="TIME")
hf_time_selected = StringVar(value="DATE")
hf_tx_title = StringVar(value="TEST")
hf_tx_selected = StringVar(value="TX")
hf_rx_title = StringVar(value="TEST")
hf_rx_selected = StringVar(value="RX")

hf_ale_title = StringVar(value="ALE")
hf_ale_selected = StringVar(value="FREQ")
hf_ale_option0 = StringVar(value="SCAN")
hf_ale_option1 = StringVar(value="FREQ")
hf_ale_option2 = StringVar(value="CHAN")
hf_ale_option3 = StringVar(value="OFF")
hf_call_title = StringVar(value="CALL")
hf_call_selected = StringVar(value="S-D")
hf_adr_title = StringVar(value="SELF ADR")
hf_adr_selected = StringVar(value="A12")
hf_freq_title = StringVar(value="FREQ")
hf_freq_selected = StringVar(value="02.000")
hf_lp_title = StringVar(value="LP")
hf_lp_selected = StringVar(value="ON")

vhf_sql_title = StringVar(value="SQL")
vhf_sql_selected = StringVar(value="OFF")
vhf_off_title = StringVar(value="OFF")
vhf_off_selected = StringVar(value="8.33")
vhf_test_title = StringVar(value="TEST")
vhf_ch_title = StringVar(value="CH")

test_page_title = StringVar(value="PREFLIGHT")
test_page_atc_title = StringVar(value="ATC:")
test_page_atc_description = StringVar(value="GO")
test_page_vl_title = StringVar(value="V/L:")
test_page_vl_description = StringVar(value="NO GO")
test_page_adf_title = StringVar(value="ADF:")
test_page_adf_description = StringVar(value="GO")
test_page_dme_title = StringVar(value="DME:")
test_page_dme_description = StringVar(value="NO GO")
test_page_uhf_title = StringVar(value="V/U:")
test_page_uhf_description = StringVar(value="GO")
test_page_hf_title = StringVar(value="HF:")
test_page_hf_description = StringVar(value="GO")
test_page_vhf_title = StringVar(value="VHF:")
test_page_vhf_description = StringVar(value="GO")
test_page_test = StringVar(value="test")
test_page_left_arrow = StringVar(value="<")
test_page_right_arrow = StringVar(value=">")
test_page_run = StringVar(value="run")
test_page_valid = StringVar(value="valid")

page_not_developed_pt1 = StringVar(value="Page not")
page_not_developed_pt2 = StringVar(value="Developed")

# Define grids
main_page.columnconfigure((0, 1), weight=1)
main_page.rowconfigure((0, 1, 2, 3), weight=1)

advanced_page.columnconfigure((0, 1), weight=1)
advanced_page.rowconfigure((0, 1, 2, 3), weight=1)

test_page.columnconfigure(0, weight=1)
test_page.rowconfigure((0, 8, 9), weight=2)
test_page.rowconfigure((1, 2, 3, 4, 5, 6, 7), weight=1)

# Define areas
main_area_1 = Main_box(main_page, uhf_active, uhf_preset, "gray")
main_area_2 = Main_box(main_page, hf_active, hf_preset, "gray")
main_area_3 = Main_box(main_page, atc_active, atc_preset, "gray")
main_area_4 = Main_box(main_page, vhf_active, vhf_preset, "gray")
main_area_5 = Main_box(main_page, vor_active, vor_preset, "gray")
main_area_6 = Main_box(main_page, adf_active, adf_preset, "gray")

advanced_area_1 = Main_box(advanced_page, var_advanced_active, var_advanced_preset, "gray")
advanced_area_2 = Advanced_box(advanced_page, "gray", 9, 1, 4)
advanced_area_3 = Advanced_box(advanced_page, "gray", 9, 1, 4)
advanced_area_4 = Advanced_box(advanced_page, "gray", 4, 1, 9)
advanced_area_5 = Advanced_box(advanced_page, "gray", 4, 1, 9)
advanced_area_6 = Advanced_box(advanced_page, "gray", 4, 1, 9)

advanced_area_2_title = Advanced_sub_box_title(advanced_area_2, var_advanced_hf_title, var_advanced_hf_selected, "left")
advanced_area_2_arrow = Advanced_sub_box_arrow(advanced_area_2, "left", uhf_sql_arrow_position)
advanced_area_2_body = Advanced_sub_box_body(advanced_area_2, "left", var_advanced_hf_option0, var_advanced_hf_option1, var_advanced_hf_option2, var_advanced_hf_option3)
advanced_area_3_title = Advanced_sub_box_title(advanced_area_3, var_advanced_atc_title, var_advanced_atc_selected, "left")
advanced_area_3_arrow = Advanced_sub_box_arrow(advanced_area_3, "left", uhf_aj_arrow_position)
advanced_area_3_body = Advanced_sub_box_body(advanced_area_3, "left", var_advanced_atc_option0, var_advanced_atc_option1, var_advanced_atc_option2, var_advanced_atc_option3)
advanced_area_4_title = Advanced_sub_box_title(advanced_area_4, var_advanced_vhf_title, var_advanced_vhf_selected, "right")
advanced_area_4_arrow = Advanced_sub_box_arrow(advanced_area_4, "right", uhf_mod_arrow_position)
advanced_area_4_body = Advanced_sub_box_body(advanced_area_4, "right", var_advanced_vhf_option0, var_advanced_vhf_option1, var_advanced_vhf_option2, var_advanced_vhf_option3)
advanced_area_5_title = Advanced_sub_box_title(advanced_area_5, var_advanced_vor_title, var_advanced_vor_selected, "right")
advanced_area_6_arrow = Advanced_sub_box_arrow(advanced_area_6, "right", uhf_mode_position)
advanced_area_5_arrow = Advanced_sub_box_arrow(advanced_area_5, "right", ufh_mar_arrow_position)
advanced_area_5_body = Advanced_sub_box_body(advanced_area_5, "right", var_advanced_vor_option0, var_advanced_vor_option1, var_advanced_vor_option2, var_advanced_vor_option3)
advanced_area_6_title = Advanced_sub_box_title(advanced_area_6, var_advanced_adf_title, var_advanced_adf_selected, "right")
advanced_area_6_body = Advanced_sub_box_body(advanced_area_6, "right", var_advanced_adf_option0, var_advanced_adf_option1, var_advanced_adf_option2, var_advanced_adf_option3)

test_area_0 = Test_big_box(test_page, test_page_title)
test_area_1 = Test_small_box(test_page, test_page_atc_title, test_page_atc_description)
test_area_2 = Test_small_box(test_page, test_page_vl_title, test_page_vl_description)
test_area_3 = Test_small_box(test_page, test_page_adf_title, test_page_adf_description)
test_area_4 = Test_small_box(test_page, test_page_dme_title, test_page_dme_description)
test_area_5 = Test_small_box(test_page, test_page_uhf_title, test_page_uhf_description)
test_area_6 = Test_small_box(test_page, test_page_hf_title, test_page_hf_description)
test_area_7 = Test_small_box(test_page, test_page_vhf_title, test_page_vhf_description)
test_area_8 = Test_big_box(test_page, test_page_test, test_page_left_arrow, test_page_right_arrow)
test_area_9 = Test_big_box(test_page, test_page_valid, test_page_run)

temporary_area_1 = Main_box(temporary_page, page_not_developed_pt1, page_not_developed_pt2, "cyan")

# Place areas in main_page
main_area_1.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
main_area_2.grid(row=1, column=0, sticky='nsew', padx=2, pady=2)
main_area_3.grid(row=2, column=0, sticky='nsew', padx=2, pady=2)
main_area_4.grid(row=0, column=1, sticky='nsew', padx=2, pady=2)
main_area_5.grid(row=1, column=1, sticky='nsew', padx=2, pady=2)
main_area_6.grid(row=2, column=1, sticky='nsew', padx=2, pady=2)

advanced_area_1.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
advanced_area_2_title.grid(row=0, column=0, sticky='nsew')
advanced_area_2_arrow.grid(row=0, column=1, sticky='nsew')
advanced_area_2_body.grid(row=0, column=2, sticky='nsew')
advanced_area_2.grid(row=1, column=0, sticky='nsew', padx=2, pady=2)

advanced_area_3_title.grid(row=0, column=0, sticky='nsew')
advanced_area_3_arrow.grid(row=0, column=1, sticky='nsew')
advanced_area_3_body.grid(row=0, column=2, sticky='nsew')
advanced_area_3.grid(row=2, column=0, sticky='nsew', padx=2, pady=2)

advanced_area_4_title.grid(row=0, column=2, sticky='nsew')
advanced_area_4_arrow.grid(row=0, column=1, sticky='nsew')
advanced_area_4_body.grid(row=0, column=0, sticky='nsew')
advanced_area_4.grid(row=0, column=1, sticky='nsew', padx=2, pady=2)

advanced_area_5_title.grid(row=0, column=2, sticky='nsew')
advanced_area_5_arrow.grid(row=0, column=1, sticky='nsew')
advanced_area_5_body.grid(row=0, column=0, sticky='nsew')
advanced_area_5.grid(row=1, column=1, sticky='nsew', padx=2, pady=2)

advanced_area_6_title.grid(row=0, column=2, sticky='nsew')
advanced_area_6_arrow.grid(row=0, column=1, sticky='nsew')
advanced_area_6_body.grid(row=0, column=0, sticky='nsew')
advanced_area_6.grid(row=2, column=1, sticky='nsew', padx=2, pady=2)

test_area_0.grid(row=0, column=0, sticky='nsew')
test_area_1.grid(row=1, column=0, sticky='nsew')
test_area_2.grid(row=2, column=0, sticky='nsew')
test_area_3.grid(row=3, column=0, sticky='nsew')
test_area_4.grid(row=4, column=0, sticky='nsew')
test_area_5.grid(row=5, column=0, sticky='nsew')
test_area_6.grid(row=6, column=0, sticky='nsew')
test_area_7.grid(row=7, column=0, sticky='nsew')
test_area_8.grid(row=8, column=0, sticky='nsew')
test_area_9.grid(row=9, column=0, sticky='nsew')

temporary_area_1.grid(row=0, column=0, sticky='nsew')

# Transponder canvases
transponder_canva_1 = Canvas(root, width=12, height=4, bg="cyan", highlightthickness=0)
transponder_canva_2 = Canvas(root, width=12, height=4, bg="cyan", highlightthickness=0)
transponder_canva_3 = Canvas(root, width=12, height=4, bg="cyan", highlightthickness=0)
transponder_canva_4 = Canvas(root, width=12, height=4, bg="cyan", highlightthickness=0)

transponder_canva_1.create_rectangle(10, 10, 400, 300, outline="#00FFFF", width=1)
transponder_canva_2.create_rectangle(10, 10, 300, 300, outline="#00FFFF", width=1)
transponder_canva_3.create_rectangle(10, 10, 300, 300, outline="#00FFFF", width=1)
transponder_canva_4.create_rectangle(10, 10, 300, 300, outline="#00FFFF", width=1)

# Create Boot Screen
boot_screen = BootScreen(root)

# Create buttons
skl_1 = Btn(root, primary_btn_img, 110, 148, lambda: side_key_push(1), lambda: keep_pressing_side_btn(1, skl_1))
skl_2 = Btn(root, primary_btn_img, 110, 232, lambda: side_key_push(2), lambda: keep_pressing_side_btn(2, skl_2))
skl_3 = Btn(root, primary_btn_img, 110, 314, lambda: side_key_push(3), lambda: keep_pressing_side_btn(3, skl_3))
skr_1 = Btn(root, primary_btn_img, 513, 148, lambda: side_key_push(4), lambda: keep_pressing_side_btn(4, skr_1))
skr_2 = Btn(root, primary_btn_img, 513, 232, lambda: side_key_push(5), lambda: keep_pressing_side_btn(5, skr_2))
skr_3 = Btn(root, primary_btn_img, 513, 314, lambda: side_key_push(6), lambda: keep_pressing_side_btn(6, skr_3))
skl_4 = Btn(root, primary_btn_img, 110, 378, lambda: print("Testando 7"), lambda: print("Testando 7 Right"))

# Buttons at the top
brt_button = Black_btn(root, off_btn_img if 'off_btn_img' in dir() else None, 105, 54, lambda: turn_on_off())
Btn(root, pge_btn_img if 'pge_btn_img' in dir() else None, 311, 45, lambda: key_up3_push())
Btn(root, key_up4_btn_img if 'key_up4_btn_img' in dir() else None, 375, 45, lambda: key_up4_push())
Btn(root, seta_btn_img if 'seta_btn_img' in dir() else None, 439, 45, lambda: print("seta btn"))
emergency_button = Btn(root, pino_left_img if 'pino_left_img' in dir() else None, 210, 50, lambda: emergency())
zeroise_button = Btn(root, pino_left_img if 'pino_left_img' in dir() else None, 532, 50, lambda: zeroise())

# Buttons at the bottom
Btn(root, atc_btn_img if 'atc_btn_img' in dir() else None, 175, 470, lambda: atc_btn_push())
Btn(root, idt_btn_img if 'idt_btn_img' in dir() else None, 243, 470, lambda: print("idt btn"))
Btn(root, triangulo_01_btn_img if 'triangulo_01_btn_img' in dir() else None, 311, 470, lambda: print("triangulo btn"))
Btn(root, triangulo_02_btn_img if 'triangulo_02_btn_img' in dir() else None, 379, 470, lambda: print("triangulo btn"))
Btn(root, ch_btn_img if 'ch_btn_img' in dir() else None, 447, 470, lambda: log())
Btn(root, freq_img if 'freq_img' in dir() else None, 507, 435, lambda: side_key_push(0))

# Frequency control buttons
Btn(root, minus if 'minus' in dir() else None, 516, 475, lambda: change_frequency(is_outer_knob=True, is_increment=False))
Btn(root, plus if 'plus' in dir() else None, 581, 475, lambda: change_frequency(is_outer_knob=True, is_increment=True))
Btn(root, minus if 'minus' in dir() else None, 540, 475, lambda: change_frequency(is_outer_knob=False, is_increment=False))
Btn(root, plus if 'plus' in dir() else None, 555, 475, lambda: change_frequency(is_outer_knob=False, is_increment=True))

# Quit button
button_quit = Button(root, text="Fechar simulador", padx=15, pady=5, command=root.quit)
button_quit.pack()

# Initialize program - começa desligado
update_screen()
update_page_icon()
get_transponder_indicator()

root.mainloop()