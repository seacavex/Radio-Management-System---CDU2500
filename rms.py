from tkinter import *           # Interface gráfica
from tkinter.font import Font   # Fontes
from PIL import ImageTk, Image  # Manipulação de Imagens
import time

# Global variables
active_area = 1                 # Área ativa (1-6) - qual rádio está selecionado
current_level = 0              # Nível de interface (0-off, 1-main freq, 2-advance, 4-teste, 5-não desenvolvida)
current_radio = 1               # Rádio selecionado
current_page = 1                # Página atual
pressed_side_btn = 0            # Click mouse direito ("clique longo")
transponder_indicator = 0
zeroise_value = False           # Estado especial 1
emergency_value = False         # Estado especial 2
start_time = None
timer = None
boot_screen_active = False      # Controla se a tela de boot está ativa
boot_start_time = None          # Armazena quando a tela de boot foi mostrada
delayinit = 2

# Manual constants
# Dimensões da tela
x_screen = 287
y_screen = 169
# screen_width = 457
# screen_height = 459
screen_width = 454
screen_height = 459
padx_screen = 2
pady_screen = 4
padx_area = 1
pady_area = 1

# Automatic  constants
full_area_width = screen_width - 2 * padx_screen
main_area_width = (screen_width - 2 * padx_screen - 2 * padx_area) / 2
main_area_height = (screen_height - 2 * pady_screen - 6 * pady_area) * 10 / 37
test_big_box_height = ( screen_height - 2 * pady_screen ) * 2 / 13
test_small_box_height = ( screen_height - 2 * pady_screen ) / 13

# Function to help programming and debugginh
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
    uhf_active.set("120.15")
    uhf_preset.set("118.15")
    hf_active.set("03.601")
    hf_preset.set("02.000")
    atc_active.set("STBY")
    atc_preset.set("2365")
    vhf_active.set("139.50")
    vhf_preset.set("136.00")
    vor_active.set("112.60")
    vor_preset.set("115.40")
    adf_active.set("430.0")
    adf_preset.set("275.0")

# Set all variables to emergency values
def set_emergency_values():
    uhf_active.set("243.00")
    uhf_preset.set("EMER")
    hf_active.set("EMER2")
    hf_preset.set("EMER1")
    atc_active.set("7700")
    atc_preset.set("EMER")
    vhf_active.set("121.50")
    vhf_preset.set("EMER")
    vor_active.set("112.60")
    vor_preset.set("115.40")
    adf_active.set("430.0")
    adf_preset.set("275.0")

    
# Reset all variables to default values
def set_zeroize():
    uhf_active.set("000.00")
    uhf_preset.set("000.00")
    hf_active.set("00.000")
    hf_preset.set("00.000")
    atc_active.set("0000")
    atc_preset.set("0000")
    vhf_active.set("000.00")
    vhf_preset.set("000.00")
    vor_active.set("000.00")
    vor_preset.set("000.00")
    adf_active.set("000.0")
    adf_preset.set("000.0")

# Function to handle the screen in case the zeroise pin is set
def zeroise():
    global zeroise_value
    zeroise_value = not zeroise_value

    print(f"Zerioze = {zeroise_value}")
    
    if zeroise_value:
        # Reset all variables to default values
        set_zeroize()
    else:
        set_default()

    update_pino_button_image(zeroise_value, zeroise_button)

# Function to handle the screen in case the emergency pin is set
def emergency():
    global emergency_value
    emergency_value = not emergency_value

    if emergency_value:
        set_emergency_values()
        main_area_3.turn_label_on(main_area_3.stby_label) # Turn label on in case it was off

    else:
        set_default()
        main_area_3.turn_label_on(main_area_3.stby_label) # Turn label on in case it was off

    update_pino_button_image(emergency_value, emergency_button)

# Handles the change of background images of pino btn
def update_pino_button_image(value, button):
    button.update_image(pino_right_img) if value else button.update_image(pino_left_img)

# Function to remove all pages of the screen
# Used before placing a page into the screen to avoid overplacement
# Add every new page created to it
def forget_all_pages():
    off_screen.place_forget()
    main_page.place_forget()
    advanced_page.place_forget()
    test_page.place_forget()
    temporary_page.place_forget() 
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

# todo
def get_transponder_indicator():
    global transponder_indicator

    if transponder_indicator == 0:
        forget_transponder_indicators()
        return
    
    if transponder_indicator == 1:
        forget_transponder_indicators()
        transponder_canva_1.place(x=363, y=531)

    if transponder_indicator == 2:
        forget_transponder_indicators()
        transponder_canva_2.place(x=382, y=531)

    if transponder_indicator == 3:
        forget_transponder_indicators()
        transponder_canva_3.place(x=402, y=531)

    if transponder_indicator == 4:
        forget_transponder_indicators()
        transponder_canva_4.place(x=421, y=531)

# Function to clear the page indicator image
# This function must always be called before placing a new page icon
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
# It already places the icons at the correct position
def place_page_icon(widget):
    forget_page_icon()
    print("icone adicionado")
    widget.place(x=690, y=565)

# Function to update the image indicator of the page based of the values of the global variables
def update_page_icon():
    global current_level, current_radio, current_page

    if current_level in {0, 4, 5}:
        #Remover indicação de páginas no rodapé
        forget_page_icon()
        forget_transponder_indicators()
        return
    
    if current_level == 1:
        if current_page == 1:
            place_page_icon(widget_page_1_2)
        elif current_page == 2:
            place_page_icon(widget_page_2_2)

    if current_level == 2:
        if current_radio == 1 or current_radio == 2:
            if current_page == 1:
                place_page_icon(widget_page_1_3)
            elif current_page == 2:
                place_page_icon(widget_page_2_3)
            elif current_page == 3:
                place_page_icon(widget_page_3_3)

# Function to update the content os the screen given its global variables
# Define qual página será exibida
def update_screen():
    # Logic to select the correct screen based on global variables  
    global active_area, current_level, current_radio, current_page
    print("Global: {}, {}, {}, {}, ".format(active_area, current_level, current_radio, current_page))

 
    if current_level not in {0, 1, 2, 3, 4, 5}:
        print(f"Erro ao mudar de nível entre as páginas na função update_screen(). Current_level = {current_level}")
        return
    
    print(current_level)

    if current_level == 0:
        print("Turning off at update_screen")

        #Remover todas as paginas
        forget_all_pages()

        #Atualizar indicação de página no rodapé (current_level == 0, remove indicação)
        update_page_icon()

        #Posiciona frame preto
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
        main_page.place(x=x_screen, y=y_screen) # Fundo
        activate_main(1)
        return
    
    if current_level == 2:

        forget_all_pages()
        update_page_icon()
        advanced_page.place(x=x_screen, y=y_screen)
        activate_advanced(1)

        # advanced_area_2_title.title.config(text=uhf_sql_title.get())
        # advanced_area_2_body.option_labels[0].config(text=uhf_sql_selected.get())
        # advanced_area_2_arrow.arrow_labels[uhf_sql_arrow_value.get()].config(text='>')
    else:
        print(f"Else statement. Area: {active_area}, Level: {current_level}, Radio: {current_radio}, Page: {current_page}")

def check_boot_complete():
    """Verifica se os 5 segundos de boot já passaram"""
    global current_level, boot_screen_active, boot_start_time, delayinit
    
    if not boot_screen_active:
        return
    
    elapsed = time.time() - boot_start_time
    
    # Atualiza a barra de progresso
    boot_screen.update_progress(int(elapsed))
    
    if elapsed >= delayinit:  # 10 segundos passaram
        # Mostra mensagem final antes de sair
        boot_screen.update_progress(10)  # Força 100%
        root.update()  # Atualiza a tela
        
        # Pequena pausa para mostrar 100%
        time.sleep(0.5)
        
        # Terminou o boot
        boot_screen_active = False
        current_level = 1
        boot_screen.place_forget()
        update_screen()
    else:
        # Ainda não terminou, verifica novamente em 100ms
        root.after(100, check_boot_complete)

# Function to turn the screen off
# It was created a current_level of 0 to the off screen
def turn_on_off():
    global current_level, boot_screen_active, boot_start_time

    print("current level", current_level)
    if current_level == 0: # Estava desligado, vai ligar
        # Mostra tela de boot primeiro
        forget_all_pages()
        boot_screen.place(x=x_screen, y=y_screen)
        boot_screen_active = True
        boot_start_time = time.time()  # Marca quando começou
        
        # Muda o ícone do botão
        brt_button.update_image(on_btn_img)
        
        # Agenda a transição para a tela principal
        check_boot_complete()
        
    else:
        current_level = 0
        boot_screen_active = False
        brt_button.update_image(off_btn_img)
        update_screen()

# Change the value of the stand by frequency of the active area
#Controle de frequência
def change_frequency(is_outer_knob, is_increment):
    global active_area, zeroise_value, emergency_value, transponder_indicator

    areas = [ main_area_1, main_area_2, main_area_3, main_area_4, main_area_5, main_area_6 ]
    print("set frequencia")
    if zeroise_value:
        return 

    # Determine which variable to use based on the current active area
    if active_area == 1 and emergency_value != True:
        delta = 1 if is_outer_knob else 0.25
        stby_var = uhf_preset
        decimals = 2
        min_freq = 225.00
        max_freq = 399.75
    elif active_area == 2 and emergency_value != True:
        delta = 0.1 if is_outer_knob else 0.001
        stby_var = hf_preset
        decimals = 3
        min_freq = 2.000
        max_freq = 29.000
    elif active_area == 3 and atc_active.get() == "STBY" and emergency_value != True:
        if is_outer_knob:
            if is_increment:
                # Increase transponder_indicator, rollover from 4 to 1
                transponder_indicator += 1
                if transponder_indicator > 4:
                    transponder_indicator = 1
                get_transponder_indicator()
            else:
                # Decrease transponder_indicator, rollover from 1 to 4
                transponder_indicator -= 1
                if transponder_indicator < 1:
                    transponder_indicator = 4
                get_transponder_indicator()
        else:
            # Set stby_var for frequency manipulation
            stby_var = atc_preset

            # Change the digit based on transponder_indicator
            current_value = int(stby_var.get())  # Convert to integer for manipulation

            if transponder_indicator == 1:  # First digit
                current_value = current_value + 1000 if is_increment else current_value - 1000
            elif transponder_indicator == 2:  # Second digit
                current_value = current_value + 100 if is_increment else current_value - 100
            elif transponder_indicator == 3:  # Third digit
                current_value = current_value + 10 if is_increment else current_value - 10
            elif transponder_indicator == 4:  # Fourth digit
                current_value = current_value + 1 if is_increment else current_value - 1
            
            # Ensure the value stays within 0000 to 7999
            current_value = current_value % 8000
            
            # Format the new value as a 4-digit string
            formatted_value = f"{current_value:04d}"
            stby_var.set(formatted_value)
            areas[active_area - 1].update_labels()

        stby_var = atc_preset 
        decimals = 0
        min_freq = 0000
        max_freq = 7999

        return

    elif active_area == 4 and emergency_value != True:
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
        # Default case if no active area is matched
        return

    current_value = float(stby_var.get())
    new_value = current_value + delta if is_increment else current_value - delta

    if new_value > max_freq:
        new_value = min_freq
    elif new_value < min_freq:
        new_value = max_freq

    # Format the new value with the specified number of decimal places
    formatted_value = f"{new_value:.{decimals}f}"

    stby_var.set(formatted_value)
    areas[active_area - 1].update_labels()

# Remove the cyan border of all areas
# This function is used in order to activate different areas of the screen
def deactivate_main_areas():
    areas = [ main_area_1, main_area_2, main_area_3, main_area_4, main_area_5, main_area_6 ]

    # Set the background color of all areas to gray
    # Contorno de seleção dos rádios
    for area in areas:
        area.config(bg="gray")
        area.update_labels()

# Set the border to cyan of the given area of the screen
def activate_main(main_area_number):
    global active_area, transponder_indicator

    areas = [ main_area_1, main_area_2, main_area_3, main_area_4, main_area_5, main_area_6 ]

    # Deactivate all areas first to ensure only one area is active at a time
    transponder_indicator = 0
    # Sublinha digito do transponder
    get_transponder_indicator()
    # Contorno de seleção em cinza
    deactivate_main_areas()

    # Activate the selected area
    if main_area_number > len(areas) or main_area_number < 1:
        return

    selected_area = areas[main_area_number - 1]
    selected_area.config(bg="cyan")
    active_area = main_area_number

    if active_area == 3:
        transponder_indicator = 1
        get_transponder_indicator()

def deactivate_advanced_areas():
    areas = [ advanced_area_1_1, advanced_area_1_2, advanced_area_1_3, advanced_area_1_4, advanced_area_1_5, advanced_area_1_6 ]

    # Set the background color of all areas to gray
    for area in areas:
        area.config(bg="gray")
        area.update_labels()

def activate_advanced(advanced_area_number):
    global active_area

    areas = [ advanced_area_1_1, advanced_area_1_2, advanced_area_1_3, advanced_area_1_4, advanced_area_1_5, advanced_area_1_6 ]

    # Deactivate all areas first to ensure only one area is active at a time
    deactivate_advanced_areas()

    # Activate the selected area
    if advanced_area_number > len(areas) or advanced_area_number < 1:
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

#  Function to get the value to be set to the advances page variables
# This functions checks the page to be displayed with the global variables and get the proper values
def get_advanced_variables():
    global current_level, current_radio, current_page
    global uhf_sql_arrow_position
    
    if current_level != 2:
        print("Error: Current level is not 2. Cannot access advanced variables.")
        return
    
    if current_radio == 1 and current_page == 1:
        # Show the advanced variables directly
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
        uhf_sql_arrow_position = 3
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
        # Show temporary variables
        var_advanced_active.set("Temporary Active")
        var_advanced_preset.set("Temporary Preset")

    update_screen() 

# Function to handle the change of pages
# This function is run when PGE button is pressed
def key_up3_push():
    global current_level, zeroise_value, emergency_value
    global active_area, current_level, current_radio, current_page

    if current_level not in {0, 1, 2, 3, 4, 5}:
        print(f"Erro ao mudar de página do nível atual. Current_level = {current_level}. Current_page = {current_page}")
        return
    
    if zeroise_value or emergency_value:
        return
    
    if current_level != 2:
        print("NÃO TEM PRÓXIMA PAG PARA ACESSAR")
        return

    if current_radio == 1:
        if current_page == 1:
            current_page = 2
        elif current_page == 2:
            current_page = 3 
        elif current_page == 3:
            current_page = 1
    elif current_radio == 2:
        if current_page == 1:
            current_page = 2
        elif current_page == 2:
            current_page = 3
        elif current_page == 3:
            current_page = 1 

    get_advanced_variables()

# Function to handle the change of level
# This function is run when VA button is pressed
def key_up4_push():
    global current_level, zeroise_value, emergency_value, current_page
    global active_area, current_level, current_radio, current_page

    if zeroise_value or emergency_value:
        return
    
    if current_level not in {0, 1, 2, 3, 4, 5}:
        print(f"Erro ao mudar de nível entre as páginas. Current_level = {current_level}")
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
    
# Function do switch the value between active and preset(stby) values
def switch_active_and_preset(active_vars, stby_vars, idx):
    print("In switch active preset")
    current_value = active_vars[idx].get()
    standby_value = stby_vars[idx].get()

    active_vars[idx].set(standby_value)
    stby_vars[idx].set(current_value)

# Function 
def toggle_area(side_key_number):
    global active_area, emergency_value, zeroise_value
    global uhf_active, uhf_preset, hf_active, hf_preset, atc_active, atc_preset
    global vhf_active, vhf_preset, vor_active, vor_preset, adf_active, adf_preset

    # Mapping variable values
    active_vars = [
        uhf_active, hf_active, atc_active, vhf_active, vor_active, adf_active
    ]
    stby_vars = [
        uhf_preset, hf_preset, atc_preset, vhf_preset, vor_preset, adf_preset
    ]

    if active_area < 1 or active_area > 7 or zeroise_value:
        return
    
    if emergency_value:
        if side_key_number == 0:
            if active_area in {1, 2, 3, 4}:
                return
            else:
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
            else:
                active_area = side_key_number
                activate_main(active_area)
                return
    # Primeiro clique em área não selecionada
    if side_key_number != 0 and side_key_number != active_area:
        active_area = side_key_number
        activate_main(active_area)
        return
 
    # Handle each case based on the active area
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
    # Returns the next non-empty option value from the provided list of options
    for option in options:
        if option.get() != "":
            if option.get() != current_value:
                return option.get()
    return current_value 

def configure_area(side_key_number): 
    global active_area, emergency_value, zeroise_value

    if active_area < 1 or active_area > 7:
        return

    if zeroise_value or emergency_value:
        return
      
    if side_key_number != 0 and side_key_number != active_area:
        active_area = side_key_number
        activate_advanced(side_key_number)
        return
    
    if active_area == 1:
        toggle_area(1)

    if current_radio == 1:
        if current_page == 1:
            if active_area == 2:
                advanced_area_1_2_nivel.set_nivel()
            if active_area == 3:
                advanced_area_1_3_selecao.set_selecao()
            if active_area == 4:
                if advanced_area_1_4.get_label_cod1() == "OFF":
                    advanced_area_1_4.set_label_cod1("ON", "cyan", "e")
                else:
                    advanced_area_1_4.set_label_cod1("OFF", "cyan", "e")
            if active_area == 5:
                if advanced_area_1_5.get_label_cod1() == "AM":
                    advanced_area_1_5.set_label_cod1("FM", "cyan", "e")
                else:
                    advanced_area_1_5.set_label_cod1("AM", "cyan", "e")
            if active_area == 6:
                advanced_area_1_6_selecao.set_selecao()

    


def side_key_push(side_key_number):
    print('Clique esquerdo, botão {}'.format(side_key_number))
    #side_key_number: número da tecla lateral

    global current_level, current_page, pressed_side_btn, active_area, transponder_indicator
    
    print("current_level: {}, current_page: {}, pressed_side_btn: {}, active_area: {}, transponder_indicator: {}".format(current_level, current_page, pressed_side_btn, active_area, transponder_indicator))

    #Se tiver algum botão segurado.
    if pressed_side_btn != 0:
        if pressed_side_btn == 3 and side_key_number == 6:
            transponder_indicator = 0
            forget_transponder_indicators()
            current_level = 4
            show_test_page()

        pressed_side_btn = 0
        unpress_side_buttons()
        return

    # Página inicial
    if current_level == 1 and current_page == 1:
        toggle_area(side_key_number)
    # Páginas avançadas
    elif current_level == 2:
        configure_area(side_key_number)

    # Páginas não desenvolvidas 
    else:
        print("Erro de páginas do sistema")

# Function to handle transponder when ATC button is pressed
def atc_btn_push():
    global active_area, emergency_value, zeroise_value

    if emergency_value or zeroise_value:
        return

    toggle_area(3)

# Function to reset the side buttons long press
def unpress_side_buttons():
    global pressed_side_btn

    skl_1.update_image(primary_btn_img)
    skl_2.update_image(primary_btn_img)
    skl_3.update_image(primary_btn_img)
    skr_1.update_image(primary_btn_img)
    skr_2.update_image(primary_btn_img)
    skr_3.update_image(primary_btn_img)

# Function to handle a long press at a side key button
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

# Class of a button, to be used in all main buttons of the screen
# It defines what must be done when the user clicks or right clicks at it
# Botão personalizado com suporte a clique direito/esquerdo
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

            # Bind mouse buttons to the button
        self.button.bind("<Button-1>", self.left_click)  # Left click
        self.button.bind("<Button-2>", self.right_click)  # Right click
        self.button.bind("<Button-3>", self.right_click)  # Right click

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

# Área principal que mostra frequencia Ativa/Standby
class Main_box(Frame):
    def __init__(self, root, ind, cod0, cod1, cod2, rspan, ncol, active, stby, bg):
        super().__init__(root, padx=padx_area, pady=pady_area, bg=bg, width=main_area_width, height=main_area_height)
        self.grid_propagate(False)
        self.ncol = ncol

        self.active_label = Label(
            self,
            textvariable=active,
            font=active_font,
            background="black",
            fg="cyan",
        )
        self.stby_label = Label(
            self,
            textvariable=stby,
            font=stby_font,
            background="black",
            fg="white",
        )
        
        self.ind_label = Label(
            self,
            textvariable=ind,
            font=ind_font,
            background="black",
            fg="white",
        )
        
        self.cod0_label = Label(
            self,
            textvariable=cod0,
            font=cod_font,
            background="black",
            fg="white",
        )
        
        self.cod1_label = Label(
            self,
            textvariable=cod1,
            font=cod_font,
            background="black",
            fg="white",
        )
        
        self.cod2_label = Label(
            self,
            textvariable=cod2,
            font=cod_font,
            background="black",
            fg="white",
        )
        self.grid_columnconfigure(0, weight=1, uniform='coluna')
        self.grid_columnconfigure(1, weight=1, minsize=110)
        self.grid_columnconfigure(2, weight=1, uniform='coluna')
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.active_label.grid(row=0, column=1, sticky='nsew')
        Label(self, bg='black').grid(row=1, column=1, sticky='nsew')
        self.stby_label.grid(row=2, column=1, sticky='nsew')
        if self.ncol == 0:
            self.ind_label.grid(row=0, column=0, rowspan=3, sticky='nsew')
            self.cod0_label.grid(row=0, column=2, rowspan=rspan, sticky='nsew')
            self.cod1_label.grid(row=1, column=2, sticky='nsew')
            self.cod2_label.grid(row=2, column=2, sticky='nsew')
        elif self.ncol == 1:
            self.cod0_label.grid(row=0, column=0, rowspan=rspan, sticky='nsew')
            self.cod1_label.grid(row=1, column=0, sticky='nsew')
            self.cod2_label.grid(row=2, column=0, sticky='nsew')
            self.ind_label.grid(row=0, column=2, rowspan=3, sticky='nsew')
        self.grid(sticky='nsew')

    def turn_label_off(self, label):
        label.config(fg="black")  # Hide label text by setting the font color to black

    def turn_label_on(self, label):
        if label == self.active_label:
            label.config(fg="cyan")  # Active label color
        elif label == self.stby_label:
            label.config(fg="white")  # Standby label color
        elif label == self.ind_label:
            label.config(fg="white")  # Standby label color

    def set_label_cod0(self, cod0, color, anchor):
        self.cod0_label.config(textvariable=StringVar(value=cod0))
        self.cod0_label.config(fg=color)
        self.cod0_label.config(anchor=anchor)

    def set_label_cod1(self, cod1, color, anchor):
        self.cod1_label.config(textvariable=StringVar(value=cod1))
        self.cod1_label.config(fg=color)
        self.cod1_label.config(anchor=anchor)

    def set_label_cod2(self, cod2, color, anchor):
        self.cod2_label.config(textvariable=StringVar(value=cod2))
        self.cod2_label.config(fg=color)
        self.cod2_label.config(anchor=anchor)

    def set_label_active(self, active_label, color, anchor):
        self.active_label.config(textvariable=StringVar(value=active_label))
        self.cod2_label.config(fg=color)
        self.cod2_label.config(anchor=anchor)

    def set_label_standby(self, stby_label, color, anchor):
        self.stby_label.config(textvariable=StringVar(value=stby_label))
        self.cod2_label.config(fg=color)
        self.cod2_label.config(anchor=anchor)

    def update_labels(self):
        # Update labels in the area
        self.active_label.update()
        self.stby_label.update()
        self.ind_label.update()
        self.cod1_label.update()

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
        self.grid_columnconfigure((0,2), weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight= 1)
        self.title_label.grid(row=0, column=1, sticky='nswe')
        self.left_text_label.grid(row=0, column=0, sticky='nswe')
        self.right_text_label.grid(row=0, column=2, sticky='nswe')

class Test_small_box(Frame):
    def __init__(self, root, title, description=""):
        super().__init__(root, width=full_area_width, height=test_small_box_height, bg="black")
        self.grid_propagate(False)

        # Assume title and description are already StringVar instances
        self.title = title
        self.description = description

        # Create labels using StringVar
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
    def __init__(self, root, cod1, cod2, cod3):
        super().__init__(root, height=main_area_height, bg="black")
        self.grid_propagate(False)
        self.cod1 = Label(
            self,
            textvariable=cod1,
            font=stby_font,
            background="black",
            fg="white"
        )
        self.cod2 = Label(
            self,   
            textvariable=cod2,
            font=stby_font,
            background="black",
            fg="cyan"
        )
        self.cod3 = Label(
            self,   
            textvariable=cod3,
            font=stby_font,
            background="black",
            fg="cyan"
        )
        self.cod4 = Label(
            self,   
            textvariable=cod2,
            font=stby_font,
            background="black",
            fg="cyan"
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight= 1)
        self.grid_rowconfigure(1, weight= 1)
        self.cod1.grid(row=0, column=0)
        self.cod2.grid(row=1, column=0)
        self.cod3.grid(row=0, column=1)
        self.cod4.grid(row=1, column=1)


class Advanced_sub_box_arrow(Frame):
    def __init__(self, root, side, arrow_position):
        super().__init__(root, height=main_area_height, bg="black")
        self.grid_propagate(False)
        self.arrow_labels = []

        # Determine the text for the arrow based on the side
        if side == "left":
            arrow_text = ">"
        elif side == "right":
            arrow_text = "<"
        else:
            arrow_text = ""

        self.grid_rowconfigure((0,1,2,3), weight=1)
        # # Create labels for each arrow position
        # for i in range(4):
        #     arrow_label = Label(
        #         self,
        #         text='',
        #         font=arrow_font,
        #         background="black",
        #         fg="cyan"
        #     )
        #     self.arrow_labels.append(arrow_label)
        #     self.grid_rowconfigure(i, weight=1)
        #     arrow_label.grid(row=i, column=0, sticky='ew')
        
        # # Store the current arrow position and update the display
        # self.current_position = arrow_position
        # self.update_arrow()

    def update_arrow(self, new_position=None):
        """Update the arrow's position. Optionally accepts a new position."""
        if new_position is not None:
            self.current_position = new_position
            
        # Update the display of arrows based on the current position
        for i, arrow_label in enumerate(self.arrow_labels):
            arrow_label.config(text=self.arrow_text if i == self.current_position else '')
        
class Advanced_sub_box_body(Frame):
    def __init__(self, root, side, option0, option1, option2, option3):
        super().__init__(root, height=main_area_height, bg="black")
        self.grid_propagate(False)
        self.option_labels = []
        # Determine the sticky option based on the side parameter
        if side == "right":
            sticky_option = 'nsw'
        else:
            sticky_option = 'nse'

        self.option0 = Label(
            self,
            textvariable=option0,
            font=option_font,
            background="black",
            fg="white",
        )        
        self.option1 = Label(
            self,
            textvariable=option1,
            font=option_font,
            background="black",
            fg="white",
        )
        self.option2 = Label(
            self,
            textvariable=option2,
            font=option_font,
            background="black",
            fg="white",
        )
        self.option3 = Label(
            self,
            textvariable=option3,
            font=option_font,
            background="black",
            fg="white",
        )
        self.grid_rowconfigure((0,1,2,3), weight=1)
        self.option0.grid(row=0, column=0, sticky=sticky_option)
        self.option1.grid(row=1, column=0, sticky=sticky_option)
        self.option2.grid(row=2, column=0, sticky=sticky_option)
        self.option3.grid(row=3, column=0, sticky=sticky_option)
        
# Área avançada com títulos, setas e opções        
class Advanced_box(Frame):
    def __init__(self, root, cod0, cod1, cod2, cod3, rspan0, rspan2, stk0, stk1, bg, ncol):
        super().__init__(root, padx=padx_area, pady=pady_area, bg=bg, width=main_area_width, height=main_area_height)
        self.grid_propagate(False)
        self.cod0_label = Label(
            self,
            textvariable=cod0,
            font=active_font,
            background="black",
            fg="white",
        )

        self.cod1_label = Label(
            self,
            textvariable=cod1,
            font=stby_font,
            background="black",
            fg="white",
        )

        self.cod2_label = Label(
            self,
            textvariable=cod2,
            font=cod_font,
            background="black",
            fg="white",
        )

        self.cod3_label = Label(
            self,
            textvariable=cod3,
            font=cod_font,
            background="black",
            fg="white",
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        if ncol == 0:
            self.cod0_label.config(anchor="w")
            self.cod1_label.config(anchor="w")
            if rspan0 == 2:
                self.cod0_label.grid(row=0, column=0, rowspan=rspan0,  sticky=stk0)
            else:
                self.cod0_label.grid(row=0, column=0, sticky=stk0)
                self.cod1_label.grid(row=1, column=0, sticky=stk0)
            
            if rspan2 == 2:
                self.cod2_label.grid(row=0, column=1, rowspan=rspan2, sticky=stk1)
            else:
                self.cod2_label.grid(row=0, column=1, sticky=stk1)
                self.cod3_label.grid(row=1, column=1, sticky=stk1)
        else:
            self.cod2_label.config(anchor="e")
            self.cod3_label.config(anchor="e")
            if rspan0 == 2:
                self.cod0_label.grid(row=0, column=1, rowspan=rspan0,  sticky=stk0)
            else:
                self.cod0_label.grid(row=0, column=1, sticky=stk0)
                self.cod1_label.grid(row=1, column=1, sticky=stk0)
            
            if rspan2 == 2:
                self.cod2_label.grid(row=0, column=0, rowspan=rspan2, sticky=stk1)
            else:
                self.cod2_label.grid(row=0, column=0, sticky=stk1)
                self.cod3_label.grid(row=1, column=0, sticky=stk1)

        self.grid(sticky='nsew')
        

    def set_label_cod0(self, cod0, color, anchor):
        self.cod0_label.config(textvariable=StringVar(value=cod0))
        self.cod0_label.config(fg=color)
        self.cod0_label.config(anchor=anchor)

    def set_label_cod1(self, cod1, color, anchor):
        self.cod1_label.config(textvariable=StringVar(value=cod1))
        self.cod1_label.config(fg=color)
        self.cod1_label.config(anchor=anchor)

    def set_label_cod2(self, cod2, color, anchor):
        self.cod2_label.config(textvariable=StringVar(value=cod2))
        self.cod2_label.config(fg=color)
        self.cod2_label.config(anchor=anchor)

    def set_label_cod3(self, cod2, color, anchor):
        self.cod3_label.config(textvariable=StringVar(value=cod2))
        self.cod3_label.config(fg=color)
        self.cod3_label.config(anchor=anchor)

    def get_label_cod0(self):
        return self.cod0_label.cget("text")
    
    def get_label_cod1(self):
        return self.cod1_label.cget("text")
    
    def get_label_cod2(self):
        return self.cod2_label.cget("text")
    
    def get_label_cod3(self):
        return self.cod3_label.cget("text")

    def update_labels(self):
        pass

class BootScreen(Frame):
    def __init__(self, root):
        super().__init__(root, width=screen_width, height=screen_height, bg="black")
        self.grid_propagate(False)
        
        # Fontes
        self.title_font = Font(family='Miriam Mono CLM', size=30, weight='bold')
        self.text_font = Font(family='Miriam Mono CLM', size=15, weight='bold')
        
        # Container principal com grid de 2 colunas
        self.main_container = Frame(self, bg="black")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center", width=457, height=459)

        pady_text = 0
        
        # Configurar grid do container principal (10 linhas, 2 colunas)
        for row in range(7):
            self.main_container.grid_rowconfigure(row, weight=0)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        
        # Título centralizado (ocupa 2 colunas na primeira linha)
        self.title_label = Label(
            self.main_container,
            text="TEST\nIN\nPROGRESS",
            font=self.title_font,
            background="black",
            fg="white",
            anchor="center"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=(100, 50))
        
        # Primeira coluna (esquerda)
        self.left_col_start = 1  # Começa na linha 1
        
        self.line_bo = Label(
            self.main_container,
            text="BO: F2FB",
            font=self.text_font,
            background="black",
            fg="white",
            anchor="w"
        )
        self.line_bo.grid(row=1, column=0, sticky='nsew', padx=(2, 2), pady=pady_text)
        
        self.line_dl = Label(
            self.main_container,
            text="DL: 6CCD",
            font=self.text_font,
            background="black",
            fg="white",
            anchor="w"
        )
        self.line_dl.grid(row=2, column=0, sticky='nsew', padx=(2, 2), pady=pady_text)
        
        self.line_bi = Label(
            self.main_container,
            text="BI: F9C6",
            font=self.text_font,
            background="black",
            fg="white",
            anchor="w"
        )
        self.line_bi.grid(row=3, column=0, sticky='nsew', padx=(2, 2), pady=pady_text)
        
        self.line_su = Label(
            self.main_container,
            text="SU: BC7B",
            font=self.text_font,
            background="black",
            fg="white",
            anchor="w"
        )
        self.line_su.grid(row=4, column=0, sticky='nsew', padx=(2, 2), pady=pady_text)
        
        self.line_co = Label(
            self.main_container,
            text="CO: BFC7",
            font=self.text_font,
            background="black",
            fg="white",
            anchor="w"
        )
        self.line_co.grid(row=5, column=0, sticky='nsew', padx=(2, 2), pady=pady_text)
        
        self.line_config = Label(
            self.main_container,
            text="CONFIG: 26AE",
            font=self.text_font,
            background="black",
            fg="black",  # Destacado em amarelo
            anchor="w"
        )
        self.line_config.grid(row=6, column=0, sticky='nsew', padx=(2, 2), pady=pady_text)
        
        # Segunda coluna (direita)
        self.line_na = Label(
            self.main_container,
            text="NA: CC53",
            font=self.text_font,
            background="black",
            fg="white",
            anchor="w"
        )
        self.line_na.grid(row=1, column=1, sticky='nsew', padx=(2, 2), pady=pady_text)
        
        self.line_cc = Label(
            self.main_container,
            text="CC: 6AC9",
            font=self.text_font,
            background="black",
            fg="white",
            anchor="w"
        )
        self.line_cc.grid(row=2, column=1, sticky='nsew', padx=(2, 2), pady=pady_text)
        
        self.line_cr = Label(
            self.main_container,
            text="CR: 1EEB",
            font=self.text_font,
            background="black",
            fg="white",
            anchor="w"
        )
        self.line_cr.grid(row=3, column=1, sticky='nsew', padx=(2, 2), pady=pady_text)
        
        self.line_tr = Label(
            self.main_container,
            text="TR: A6BE",
            font=self.text_font,
            background="black",
            fg="white",
            anchor="w"
        )
        self.line_tr.grid(row=4, column=1, sticky='nsew', padx=(2, 2), pady=pady_text)
        
        self.line_sp = Label(
            self.main_container,
            text="SP: E3B9",
            font=self.text_font,
            background="black",
            fg="white",
            anchor="w"
        )
        self.line_sp.grid(row=5, column=1, sticky='nsew', padx=(2, 2), pady=pady_text)

    
    def update_progress(self, elapsed_seconds):
        """Atualiza a mensagem de progresso baseado no tempo decorrido"""
        total_seconds = delayinit
        progress = min(int((elapsed_seconds / total_seconds) * 100), 100)
        
        if progress >= delayinit/2:
            self.line_config.config(fg="white")

        # self.progress_label.config(text=msg, fg=color)

class BarraNivel:
    def __init__(self, parent, x, y, largura=30, altura=90):
        self.canvas = Canvas(
            parent,
            width=largura,
            height=altura,
            bg='black',
            highlightthickness=0
        )
        self.canvas.place(x=x, y=y)
        
        self.altura_quadrado = altura // 3
        self.quadrados = []

        self.nivel = 3
        
        # Cria os 3 quadrados
        for i in range(3):
            y0 = i * self.altura_quadrado
            y1 = (i + 1) * self.altura_quadrado
            
            quad = self.canvas.create_rectangle(
                1, y0 + 1, largura - 1, y1 - 1,
                outline='white',
                fill='black',
                width=2
            )
            self.quadrados.append(quad)
        
        for i, cor in enumerate(['white', 'white', 'white']):
            self.canvas.itemconfig(self.quadrados[i], fill=cor)
    
    def set_nivel(self):
        self.nivel = self.nivel + 1

        if self.nivel > 3:
            self.nivel = 0

        print("Nivel: {}".format(self.nivel))
        if self.nivel == 0:
            main_area_1.set_label_cod0("$", "orange", "n")
            advanced_area_1_1.set_label_cod0("$", "orange", "n")
            advanced_area_1_2.set_label_cod1("OFF", "cyan", "w")
        if self.nivel == 1:
            main_area_1.set_label_cod0("", "black", "center")
            advanced_area_1_1.set_label_cod0("", "black", "center")
            advanced_area_1_2.set_label_cod1("LOW", "cyan", "w")
        if self.nivel == 2:
            advanced_area_1_2.set_label_cod1("MED", "cyan", "w")
        if self.nivel == 3:
            advanced_area_1_2.set_label_cod1("HI", "cyan", "w")



        cores = ['black', 'black', 'black']
        for i in range(min(self.nivel, 3)):
            cores[2 - i] = 'white'
        
        for i, cor in enumerate(cores):
            self.canvas.itemconfig(self.quadrados[i], fill=cor)


class SetaNivel4:
    def __init__(self, parent, x, y, largura=30, altura=90, cores=None):
        self.canvas = Canvas(
            parent,
            width=largura,
            height=altura,
            bg='black',
            highlightthickness=0
        )
        self.canvas.place(x=x, y=y)
        
        # Cores padrão ou personalizadas (vermelho, amarelo, verde)
        if cores is None:
            self.cores = ["#FFFFFF","#FFFFFF", '#FFFFFF', '#FFFFFF']
        else:
            self.cores = cores
        
        self.altura_triangulo = altura // 4
        self.triangulos = []
        self.nivel = 0
        
        # Cria os 3 triângulos (setas para direita)
        for i in range(4):
            y_centro = i * self.altura_triangulo + self.altura_triangulo // 2
            
            # Coordenadas do triângulo apontando para direita
            pontos = [
                10, y_centro - 10,          # Ponta esquerda superior
                largura - 5, y_centro,       # Ponta direita (meio)
                10, y_centro + 10           # Ponta esquerda inferior
            ]
            
            triangulo = self.canvas.create_polygon(
                pontos,
                outline='black',
                fill='black',
                width=2
            )
            self.triangulos.append(triangulo)

        self.set_selecao()
    
    def set_selecao(self):
        
        self.nivel += 1
        if self.nivel < 1:
            return
        if self.nivel > 4:
            self.nivel = 1
        if self.nivel == 1:
            uhf_active.set("120.15")
            uhf_preset.set("118.15")
            advanced_area_1_3.set_label_cod1("T/R", "cyan", "w")
        if self.nivel == 2:
            main_area_1.set_label_cod1("+G", "white", "e")
            advanced_area_1_1.set_label_cod1("+G", "white", "e")
            advanced_area_1_3.set_label_cod1("TR+G", "cyan", "w")
        if self.nivel == 3:
            main_area_1.set_label_cod1("", "white", "e")
            advanced_area_1_1.set_label_cod1("", "white", "e")
            uhf_active.set("243.00")
            uhf_preset.set("GUARD")
            advanced_area_1_3.set_label_cod1("243", "cyan", "w")
        if self.nivel == 4:
            uhf_active.set("121.00")
            uhf_preset.set("GUARD")
            advanced_area_1_3.set_label_cod1("121", "cyan", "w")
        
        print(self.nivel)
        
        print("Nivel seta")
        # Primeiro, apaga todas as setas
        for i in range(4):
            self.canvas.itemconfig(self.triangulos[i], outline='black')
        
        # Acende apenas a seta do nível atual com sua cor específica
        self.canvas.itemconfig(
            self.triangulos[self.nivel - 1], 
            outline=self.cores[self.nivel - 1]
        )
    
    def get_nivel(self):
        """Retorna o nível atual"""
        return self.nivel


class SetaNivel3:
    def __init__(self, parent, x, y, largura=30, altura=90, cores=None):
        self.canvas = Canvas(
            parent,
            width=largura,
            height=altura,
            bg='black',
            highlightthickness=0
        )
        self.canvas.place(x=x, y=y)
        
        # Cores padrão ou personalizadas (vermelho, amarelo, verde)
        if cores is None:
            self.cores = ["#FFFFFF","#FFFFFF", '#FFFFFF']
        else:
            self.cores = cores
        
        self.altura_triangulo = altura // 3
        self.triangulos = []
        self.nivel = 0
        
        # Cria os 3 triângulos (setas para direita)
        for i in range(3):
            y_centro = i * self.altura_triangulo + self.altura_triangulo // 2
            
            # Coordenadas do triângulo apontando para direita
            pontos = [
                largura - 5, y_centro - 10,          # Ponta esquerda superior
                10, y_centro,       # Ponta direita (meio)
                largura - 5, y_centro + 10           # Ponta esquerda inferior
            ]
            
            triangulo = self.canvas.create_polygon(
                pontos,
                outline='black',
                fill='black',
                width=2
            )
            self.triangulos.append(triangulo)

        self.set_selecao()
    
    def set_selecao(self):
        
        self.nivel += 1
        if self.nivel < 1:
            return
        if self.nivel > 3:
            self.nivel = 1
        if self.nivel == 1:
            pass
            # uhf_active.set("120.15")
            # uhf_preset.set("118.15")
            advanced_area_1_6.set_label_cod1("OFF", "cyan", "e")
        if self.nivel == 2:
            # main_area_1.set_label_cod1("+G", "white", "e")
            advanced_area_1_6.set_label_cod1("CST", "cyan", "e")
        if self.nivel == 3:
            # main_area_1.set_label_cod1("", "white", "e")
            advanced_area_1_6.set_label_cod1("SHIP", "cyan", "e")
        
        print(self.nivel)
        
        print("Nivel seta")
        # Primeiro, apaga todas as setas
        for i in range(3):
            self.canvas.itemconfig(self.triangulos[i], outline='black')
        
        # Acende apenas a seta do nível atual com sua cor específica
        self.canvas.itemconfig(
            self.triangulos[self.nivel - 1], 
            outline=self.cores[self.nivel - 1]
        )
    
    def get_nivel(self):
        """Retorna o nível atual"""
        return self.nivel


root = Tk()
root.title("Simulador RMS")
root.resizable(False, False)

# Define fonts
active_font = Font(
    family='Miriam Mono CLM',
    size=26,
    weight='bold'
)

stby_font = Font(
    family='Miriam Mono CLM',
    size=24,
    weight='bold'
)

option_font = Font(
    family='Miriam Mono CLM',
    size=8,
)

arrow_font = Font(
    family='Miriam Mono CLM',
    size=12,
)

test_body_font = Font(
    family='Miriam Mono CLM',
    size=10,
)

ind_font = Font(
    family='Miriam Mono CLM',
    size=16,
    weight='bold'
)

cod_font = Font(
    family='Miriam Mono CLM',
    size=16,
    weight='bold'
)

# Load image
# rms_image = ImageTk.PhotoImage(Image.open("Fundo_completo_11.jpeg"))    # Desenho
rms_image = ImageTk.PhotoImage(Image.open("imagens/Moldura_fundo.png"))   # Textura real
rms_label = Label(root, image=rms_image)
rms_label.pack()

# Define button images
primary_btn_img = PhotoImage(file="imagens/btn_generico_80x52.png")
primary_btn_pressed_img = PhotoImage(file="bt_ativo.png")
atc_btn_img = PhotoImage(file="imagens/bt_atc.png")
ch_btn_img = PhotoImage(file="imagens/bt_ch.png")
idt_btn_img = PhotoImage(file="imagens/bt_idt.png")
pge_btn_img = PhotoImage(file="imagens/bt_pge.png")
seta_btn_img = PhotoImage(file="imagens/bt_quadrado_riscado.png")
key_up4_btn_img = PhotoImage(file="imagens/bt_in_out.png")
triangulo_02_btn_img = PhotoImage(file="imagens/bt_tri.png")
triangulo_01_btn_img = PhotoImage(file="imagens/bt_tri.png")
freq_img = PhotoImage(file="bt_freq2.png")
on_btn_img = PhotoImage(file="imagens/bt_btc_on.png")
off_btn_img = PhotoImage(file="imagens/bt_btc_off.png")
pino_left_img = PhotoImage(file="imagens/toggle_esq.png")
pino_right_img = PhotoImage(file="imagens/toggle_dir.png")
plus = PhotoImage(file="imagens/seta_horario.png")
minus = PhotoImage(file="imagens/seta_antihorario.png")
page_1_2 = PhotoImage(file="page_1_2.png")
page_2_2 = PhotoImage(file="page_2_2.png")
page_1_3 = PhotoImage(file="page_1_3.png")
page_2_3 = PhotoImage(file="page_2_3.png")
page_3_3 = PhotoImage(file="page_3_3.png")
page_1_4 = PhotoImage(file="page_1_4.png")
page_2_4 = PhotoImage(file="page_2_4.png")
page_3_4 = PhotoImage(file="page_3_4.png")
page_4_4 = PhotoImage(file="page_4_4.png")

widget_page_1_2 = Label(root, image=page_1_2, background="#000000")
widget_page_2_2 = Label(root, image=page_2_2, background="#000000")
widget_page_1_3 = Label(root, image=page_1_3, background="#000000")
widget_page_2_3 = Label(root, image=page_2_3, background="#000000")
widget_page_3_3 = Label(root, image=page_3_3, background="#000000")
widget_page_1_4 = Label(root, image=page_1_4, background="#000000")
widget_page_2_4 = Label(root, image=page_2_4, background="#000000")
widget_page_3_4 = Label(root, image=page_3_4, background="#000000")
widget_page_4_4 = Label(root, image=page_4_4, background="#000000")



# Create Pages to be shown in  the screen
main_page = Frame(
    root,
    width=screen_width,
    height=screen_height,
    pady=pady_screen,
    bg="black",
) 

off_screen = Frame(
    root, 
    width=screen_width,
    height=screen_height,
    pady=pady_screen,
    bg="black",
)

advanced_page = Frame(
    root,
    width=screen_width,
    height=screen_height,
    pady=pady_screen,
    bg="black",
)

test_page = Frame(
    root,
    width=screen_width,
    height=screen_height,
    pady=pady_screen,
    bg="black",
)

temporary_page = Frame (
    root,
    width=screen_width,
    height=screen_height,
    pady=pady_screen,
    bg="black",
)

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

#------------ UHF -----------------------------
uhf_ind = StringVar(value="V\n/\nU")
uhf_active = StringVar(value="120.15")
uhf_preset = StringVar(value="118.15")
uhf_cod0 = StringVar(value="")
uhf_cod1 = StringVar(value="")
uhf_cod2 = StringVar(value="")
#---------- UHF ADVANCED -----------------------
uhf_advanced_2_cod0 = StringVar(value="SQL")
uhf_advanced_2_cod1 = StringVar(value="")
uhf_advanced_2_cod2 = StringVar(value="")
uhf_advanced_2_cod3 = StringVar(value="")
uhf_advanced_3_cod0 = StringVar(value="MODE")
uhf_advanced_3_cod1 = StringVar(value="T/R")
uhf_advanced_3_cod2 = StringVar(value="TR\x20\x20\nTR+G\n243\x20\n121\x20")
uhf_advanced_3_cod3 = StringVar(value="")
uhf_advanced_4_cod0 = StringVar(value="")
uhf_advanced_4_cod1 = StringVar(value="")
uhf_advanced_4_cod2 = StringVar(value="")
uhf_advanced_4_cod3 = StringVar(value="")
uhf_advanced_5_cod0 = StringVar(value="")
uhf_advanced_5_cod1 = StringVar(value="")
uhf_advanced_5_cod2 = StringVar(value="")
uhf_advanced_5_cod3 = StringVar(value="")
uhf_advanced_6_cod0 = StringVar(value="")
uhf_advanced_6_cod1 = StringVar(value="")
uhf_advanced_6_cod2 = StringVar(value="")
uhf_advanced_6_cod3 = StringVar(value="")
#------------------------------------------------
hf_ind = StringVar(value="H\nF")
hf_cod0 = StringVar(value="")
hf_cod1 = StringVar(value="")
hf_cod2 = StringVar(value="")
hf_active = StringVar(value="03.601")
hf_preset = StringVar(value="02.000")
atc_ind = StringVar(value="A\nT\nC")
atc_cod0 = StringVar(value="")
atc_cod1 = StringVar(value="")
atc_cod2 = StringVar(value="")
atc_active = StringVar(value="STBY")
atc_preset = StringVar(value="2365")
vhf_ind = StringVar(value="V\nH\nF")
vhf_cod0 = StringVar(value="")
vhf_cod1 = StringVar(value="")
vhf_cod2 = StringVar(value="")
vhf_active = StringVar(value="139.50")  
vhf_preset = StringVar(value="136.00")
vor_ind = StringVar(value="V\n/\nL")
vor_cod0 = StringVar(value="")
vor_cod1 = StringVar(value="")
vor_cod2 = StringVar(value="")
vor_active = StringVar(value="112.60")
vor_preset = StringVar(value="115.40")
adf_ind = StringVar(value="A\nD\nF")
adf_cod0 = StringVar(value="")
adf_cod1 = StringVar(value="")
adf_cod2 = StringVar(value="")
adf_active = StringVar(value="430.0")
adf_preset = StringVar(value="275.0") 

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

# Define a grid
main_page.columnconfigure((0, 1), weight=1)
main_page.rowconfigure((0, 1, 2, 3), weight=1)

advanced_page.columnconfigure((0, 1), weight=1)
advanced_page.rowconfigure((0, 1, 2, 3), weight=1)

test_page.columnconfigure(0, weight=1)
test_page.rowconfigure((0, 8, 9), weight=2)
test_page.rowconfigure((1, 2, 3, 4, 5, 6, 7), weight=1)


# Define areas Main_box(self, root, ind, cod0, cod1, cod2, rspan, ncol, active, stby, bg)
# set_label_cod(self, cod0, cod1, cod2, color, anchor)
main_area_1 = Main_box(main_page, uhf_ind, uhf_cod0, uhf_cod1, uhf_cod2,  1, 0, uhf_active, uhf_preset, "gray")
main_area_1.set_label_cod2("PT", "white", "s")
main_area_2 = Main_box(main_page, hf_ind, hf_cod0, hf_cod1, hf_cod2, 1, 0, hf_active, hf_preset, "gray")
main_area_3 = Main_box(main_page, atc_ind, atc_cod0, atc_cod1, atc_cod2, 1, 0, atc_active, atc_preset, "gray")
main_area_3.set_label_cod1("ALT", "orange", "center")
main_area_4 = Main_box(main_page, vhf_ind, vhf_cod0, vhf_cod1, vhf_cod2, 1, 1, vhf_active, vhf_preset, "gray")
main_area_5 = Main_box(main_page, vor_ind, vor_cod0, vor_cod1, vor_cod2, 1, 1, vor_active, vor_preset, "gray")
main_area_6 = Main_box(main_page, adf_ind, adf_cod0, adf_cod1, adf_cod2, 1, 1, adf_active, adf_preset, "gray")

advanced_area_1_1 = Main_box(advanced_page, uhf_ind, uhf_cod0, uhf_cod1, uhf_cod2,  1, 0, uhf_active, uhf_preset, "gray")
advanced_area_1_1.set_label_cod2("PT", "white", "s")
advanced_area_1_2 = Advanced_box(advanced_page, uhf_advanced_2_cod0, uhf_advanced_2_cod1, uhf_advanced_2_cod2, uhf_advanced_2_cod3,  1, 2, 'nsew', 'nsew', "gray", 0)
advanced_area_1_2.set_label_cod1("HI", "cyan", "w")
advanced_area_1_2_nivel = BarraNivel(advanced_area_1_2, 150, 20, 25, 75)
advanced_area_1_3 = Advanced_box(advanced_page, uhf_advanced_3_cod0, uhf_advanced_3_cod1, uhf_advanced_3_cod2, uhf_advanced_3_cod3,  1, 2, 'nsew', 'nsew', "gray", 0)
advanced_area_1_3_selecao = SetaNivel4(advanced_area_1_3, 115, 15, 30, 90)
advanced_area_1_4 = Advanced_box(advanced_page, uhf_advanced_4_cod2, uhf_advanced_4_cod3, uhf_advanced_4_cod0, uhf_advanced_4_cod1,  1, 1, 'nsew', 'nsew', "gray", 1)
advanced_area_1_4.set_label_cod0("AJ", "white", "e")
advanced_area_1_4.set_label_cod1("OFF", "cyan", "e")
advanced_area_1_5 = Advanced_box(advanced_page, uhf_advanced_5_cod2, uhf_advanced_5_cod3, uhf_advanced_5_cod0, uhf_advanced_5_cod1,  1, 1, 'nsew', 'nsew', "gray", 1)
advanced_area_1_5.set_label_cod0("MOD", "white", "e")
advanced_area_1_5.set_label_cod1("AM", "cyan", "e")
advanced_area_1_6 = Advanced_box(advanced_page, uhf_advanced_6_cod2, uhf_advanced_6_cod3, uhf_advanced_6_cod0, uhf_advanced_6_cod1,  1, 2, 'nsew', 'nsew', "gray", 1)
advanced_area_1_6_selecao = SetaNivel3(advanced_area_1_6, 90, 20, 25, 75)
advanced_area_1_6.set_label_cod0("\x20MAR", "white", "e")
advanced_area_1_6.set_label_cod1("OFF", "cyan", "e")
advanced_area_1_6.set_label_cod2("\x20OFF\n\x20CST\nSHIP", "white", "e")

# advanced_area_2_title = Advanced_sub_box_title(advanced_area_1_2, var_advanced_hf_title, var_advanced_hf_selected, "left")
# advanced_area_2_arrow = Advanced_sub_box_arrow(advanced_area_1_2, "left", uhf_sql_arrow_position)
# advanced_area_2_body = Advanced_sub_box_body(advanced_area_1_2, "left", var_advanced_hf_option0, var_advanced_hf_option1, var_advanced_hf_option2, var_advanced_hf_option3)
# advanced_area_3_title = Advanced_sub_box_title(advanced_area_1_3, var_advanced_atc_title, var_advanced_atc_selected, "left")
# advanced_area_3_arrow = Advanced_sub_box_arrow(advanced_area_1_3, "left", uhf_aj_arrow_position)
# advanced_area_3_body = Advanced_sub_box_body(advanced_area_1_3, "left", var_advanced_atc_option0, var_advanced_atc_option1, var_advanced_atc_option2, var_advanced_atc_option3)
# advanced_area_4_title = Advanced_sub_box_title(advanced_area_1_4, var_advanced_vhf_title, var_advanced_vhf_selected, "right")
# advanced_area_4_arrow = Advanced_sub_box_arrow(advanced_area_1_4, "right", uhf_mod_arrow_position)
# advanced_area_4_body = Advanced_sub_box_body(advanced_area_1_4, "right", var_advanced_vhf_option0, var_advanced_vhf_option1, var_advanced_vhf_option2, var_advanced_vhf_option3)
advanced_area_5_title = Advanced_sub_box_title(advanced_area_1_5, var_advanced_vor_title, var_advanced_vor_selected, "right")
advanced_area_6_arrow = Advanced_sub_box_arrow(advanced_area_1_6, "right", uhf_mode_position)
advanced_area_5_arrow = Advanced_sub_box_arrow(advanced_area_1_5, "right", ufh_mar_arrow_position)
advanced_area_5_body = Advanced_sub_box_body(advanced_area_1_5, "right", var_advanced_vor_option0, var_advanced_vor_option1, var_advanced_vor_option2, var_advanced_vor_option3)
advanced_area_6_title = Advanced_sub_box_title(advanced_area_1_6, var_advanced_adf_title, var_advanced_adf_selected, "right")
advanced_area_6_body = Advanced_sub_box_body(advanced_area_1_6, "right", var_advanced_adf_option0, var_advanced_adf_option1, var_advanced_adf_option2, var_advanced_adf_option3)

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

temporary_area_1 = Main_box(temporary_page, page_not_developed_pt1, page_not_developed_pt2, page_not_developed_pt1, page_not_developed_pt2,  1, 0, page_not_developed_pt2, page_not_developed_pt2, "cyan")

# Place areas in main_page areas
main_area_1.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
main_area_2.grid(row=1, column=0, sticky='nsew', padx=2, pady=2)
main_area_3.grid(row=2, column=0, sticky='nsew', padx=2, pady=2)
main_area_4.grid(row=0, column=1, sticky='nsew', padx=2, pady=2)
main_area_5.grid(row=1, column=1, sticky='nsew', padx=2, pady=2)
main_area_6.grid(row=2, column=1, sticky='nsew', padx=2, pady=2)

advanced_area_1_1.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
# advanced_area_2_title.grid(row=0, column=0, sticky='nsew')
# advanced_area_2_arrow.grid(row=0, column=1, sticky='nsew')
# advanced_area_2_body.grid(row=0, column=2, sticky='nsew')
advanced_area_1_2.grid(row=1, column=0, sticky='nsew', padx=2, pady=2)

# advanced_area_3_title.grid(row=0, column=0, sticky='nsew')
# advanced_area_3_arrow.grid(row=0, column=1, sticky='nsew')
# advanced_area_3_body.grid(row=0, column=2, sticky='nsew')
advanced_area_1_3.grid(row=2, column=0, sticky='nsew', padx=2, pady=2)

# advanced_area_4_title.grid(row=0, column=2, sticky='nsew')
# advanced_area_4_arrow.grid(row=0, column=1, sticky='nsew')
# advanced_area_4_body.grid(row=0, column=0, sticky='nsew')
advanced_area_1_4.grid(row=0, column=1, sticky='nsew', padx=2, pady=2)

# advanced_area_5_title.grid(row=0, column=2, sticky='nsew')
# advanced_area_5_arrow.grid(row=0, column=1, sticky='nsew')
# advanced_area_5_body.grid(row=0, column=0, sticky='nsew')
advanced_area_1_5.grid(row=1, column=1, sticky='nsew', padx=2, pady=2)

# advanced_area_6_title.grid(row=0, column=2, sticky='nsew')
# advanced_area_6_arrow.grid(row=0, column=1, sticky='nsew')
# advanced_area_6_body.grid(row=0, column=0, sticky='nsew')
advanced_area_1_6.grid(row=2, column=1, sticky='nsew', padx=2, pady=2)

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

transponder_canva_1 = Canvas(root, width=16, height=4, bg="cyan", highlightthickness=0)
transponder_canva_2 = Canvas(root, width=16, height=4, bg="cyan", highlightthickness=0)
transponder_canva_3 = Canvas(root, width=16, height=4, bg="cyan", highlightthickness=0)
transponder_canva_4 = Canvas(root, width=16, height=4, bg="cyan", highlightthickness=0)
    
transponder_canva_1.create_rectangle(10, 10, 400, 300, outline="#00FFFF", width=1)
transponder_canva_2.create_rectangle(10, 10, 300, 300, outline="#00FFFF", width=1)
transponder_canva_3.create_rectangle(10, 10, 300, 300, outline="#00FFFF", width=1)
transponder_canva_4.create_rectangle(10, 10, 300, 300, outline="#00FFFF", width=1)

# Create Boot Screen
boot_screen = BootScreen(root)

# Create specific buttons that will toggle the labels
# Botões de seleção dos rádios
skl_1 = Btn(root, primary_btn_img, 150, 209, lambda: side_key_push(1), lambda: keep_pressing_side_btn(1, skl_1))
skl_2 = Btn(root, primary_btn_img, 150, 332, lambda: side_key_push(2), lambda: keep_pressing_side_btn(2, skl_2))
skl_3 = Btn(root, primary_btn_img, 150, 454, lambda: side_key_push(3), lambda: keep_pressing_side_btn(3, skl_3))
skr_1 = Btn(root, primary_btn_img, 796, 209, lambda: side_key_push(4), lambda: keep_pressing_side_btn(4, skr_1))
skr_2 = Btn(root, primary_btn_img, 796, 332, lambda: side_key_push(5), lambda: keep_pressing_side_btn(5, skr_2))
skr_3 = Btn(root, primary_btn_img, 796, 454, lambda: side_key_push(6), lambda: keep_pressing_side_btn(6, skr_3))
skl_4 = Btn(root, primary_btn_img, 150, 547, lambda: print("Testando 7"), lambda: print("Testando 7 Right"))

# Buttons at the top of the screen

#Altera a imagem do botão BRT, current_level para 1, e chama update_screen
brt_button = Black_btn(root, off_btn_img, 130, 94, lambda: turn_on_off())
Btn(root, pge_btn_img, 453, 67, lambda: key_up3_push())
Btn(root, key_up4_btn_img, 558, 67, lambda: key_up4_push())
Btn(root, seta_btn_img, 663, 67, lambda: print("seta btn"))
emergency_button = Btn(root, pino_left_img, 286, 50, lambda: emergency()) # Radio
zeroise_button = Btn(root, pino_left_img, 789  , 50, lambda: zeroise())   # Zeroize

# Buttons at the bottom of the screen
Btn(root, atc_btn_img, 269, 691, lambda: atc_btn_push())
Btn(root, idt_btn_img, 373, 691, lambda: print("idt btn"))
Btn(root, triangulo_01_btn_img, 475, 691, lambda: print("triangulo btn"))
Btn(root, triangulo_02_btn_img, 578, 691, lambda: print("triangulo btn"))
Btn(root, ch_btn_img, 681, 691, lambda: log())
# Btn(root, freq_img, 817, 632, lambda: side_key_push(0))

# Temporary buttons
Btn(root, minus, 807, 670, lambda: change_frequency(is_outer_knob = True, is_increment = False))
Btn(root, plus, 913, 670, lambda: change_frequency(is_outer_knob = True, is_increment = True))
Btn(root, minus, 831, 670, lambda: change_frequency(is_outer_knob = False, is_increment = False))
Btn(root, plus, 888, 670, lambda: change_frequency(is_outer_knob = False, is_increment = True))

# Quit button
button_quit = Button(root, text="Fechar simulador", padx=15, pady=5, command=root.quit)
button_quit.pack()

# Initialize program
#Atualiza a página selecionada (current_level)
update_screen()

#Atualiza o idicador de página no rodapé
update_page_icon()

get_transponder_indicator()

root.mainloop()