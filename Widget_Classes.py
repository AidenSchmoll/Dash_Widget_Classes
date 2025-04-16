


# General imports
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *



class Warning_Light(QWidget):
    """
    @class Warning_Light
    @brief A QWidget-based warning light that displays a PNG image when activated.

    This widget is designed to show or hide a warning light image, useful in
    GUIs where visual alerts are needed. Can Be resized to fit any need when initialized.
    """

    def __init__(self, parent=None, png_path=None, height=100, width=100):
        """
        @brief Constructor for the Warning_Light widget.

        @param parent The parent widget (optional).
        @param png_path Path to the PNG image to display as the warning light.
        @param height Initial height of the widget in pixels.
        @param width Initial width of the widget in pixels.
        """
        super().__init__(parent)
        self.setStyleSheet("background-color: black;")
        self.png_path = png_path

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)

        # Load the pixmap only if the path is valid
        if self.png_path:
            pixmap = QPixmap(self.png_path)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

        self.hide()  # Initially hide the widget
        
        

    
    def show_light(self):
        """
        @brief Toggles the warning light to be "On".

        Call this function to make the warning light visible.
        """
        self.show()

    
    def hide_light(self):
        """
        @brief Toggles the warning light to be "Off".

        Call this function to make the warning light not visible.
        """
        self.hide()


    
    def resizeEvent(self, event):
        """
        @brief Handle resize events and update label and pixmap accordingly.

        This ensures the widget fills the specified area and the pixmap is scaled
        to fit while maintaining its aspect ratio.

        @param event The resize event.
        """
        super().resizeEvent(event)
        self.label.setGeometry(self.rect())  # Make the label fill the entire widget

        # Resize the pixmap to fit the label while maintaining the aspect ratio
        if self.label.pixmap():
            self.label.setPixmap(self.label.pixmap().scaled(self.label.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))




class Temp_Gauge(QWidget):
    """
    @class Temp_Gauge
    @brief A QWidget-based vertical temperature gauge with gradient fill, tick marks and a value indicator.

    This custom widget visually represents a temperature value using a colored bar,
    tick marks, and numeric labels. The bar fills from green to red as the temperature increases.
    """

    def __init__(self, parent=None, max_value=300):
        """
        @brief Constructor for the Temp_Gauge widget.

        @param parent The parent widget (optional).
        @param max_value The maximum temperature value the gauge can represent. Scales the gauge values based on this value.
        """
        super().__init__(parent)
        self.value = 0  # Initial temp gauge value
        self.max_value = max_value  # Maximum value of the temp gauge
        self.setStyleSheet("background-color: black;")

        # USED IN PLACE OF OTHER 2 fonts (FONT: "Baja")
        font_id = QFontDatabase.addApplicationFont("Fonts/Baja.ttf")
        if font_id < 0: print("ERROR")
        font_families = QFontDatabase.applicationFontFamilies(font_id)


    def add_to_value(self, change):
        """
        @brief Add to the temperature gauge value.

        @param change The add amount to change the current value by.
        The new value wraps around if it exceeds the max value.
        """
        # Update the temp gauge value
        self.value = (self.value + change) % (self.max_value + 1)
        self.update()  # Request a redraw

    def update_value(self, new_value):
        """
        @brief Update the temperature gauge value.

        @param new_value The new value for the gauge to be set to.
        The new value wraps around if it exceeds the max value.
        """
        # Update the temp gauge value
        self.value = new_value % (self.max_value + 1)
        self.update()  # Request a redraw

    def paintEvent(self, event):
        """
        @brief Handle the paint event for rendering the gauge.

        This method draws the temperature bar, gradient fill, tick marks, and text labels.
        It also includes a circle and value/unit display. Also handles resizing.
        
        @param event The paint event triggered by Qt.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        size_factor = min(width, height) / 2 * 0.7

        bar_center_y = center_y - size_factor*.15
        


        # Draw the gauge (Grey backing)
        gauge_size = .1*size_factor
        painter.setPen(QPen(QColor(150,150,150), gauge_size))


        painter.drawLine(center_x, bar_center_y + size_factor, center_x, bar_center_y - size_factor)

        # Gauge Gradient
        self.gaugeGrad = QLinearGradient(QPointF(center_x, bar_center_y - size_factor), QPointF(center_x, bar_center_y + size_factor))
        self.gaugeGrad.setColorAt(1, Qt.green)
        self.gaugeGrad.setColorAt(0.2, Qt.yellow)
        self.gaugeGrad.setColorAt(0, Qt.red)

        # Draw the value indicator 
        painter.setPen(QPen(self.gaugeGrad, gauge_size))

        # Gauge Fill to value

        length = (self.value / (self.max_value*.5)) * size_factor

        if length >= 0:
            painter.drawLine(center_x, bar_center_y + size_factor, center_x, bar_center_y + size_factor - length)
        else:
            None

        # Draw the tick marks
        painter.setPen(QPen(QColor(255,255,255), 5))
        Font = QFont("Baja", size_factor*.05)
        painter.setFont(Font)

        # Last tick (MAX VALUE)
        painter.drawLine(center_x - gauge_size*.5, bar_center_y - size_factor - gauge_size*.5, center_x + gauge_size*.5, bar_center_y - size_factor - gauge_size*.5)
        painter.drawText(center_x - gauge_size*2, bar_center_y - size_factor, f"{self.max_value}")

        painter.drawLine(center_x - gauge_size*.4, bar_center_y - size_factor*4/5 - gauge_size*.5, center_x + gauge_size*.4, bar_center_y - size_factor*4/5 - gauge_size*.5)

        painter.drawLine(center_x - gauge_size*.5, bar_center_y - size_factor*3/5 - gauge_size*.5, center_x + gauge_size*.5, bar_center_y - size_factor*3/5 - gauge_size*.5)
        painter.drawText(center_x - gauge_size*2, bar_center_y - size_factor*3/5, f"{int(self.max_value*4/5)}")

        painter.drawLine(center_x - gauge_size*.4, bar_center_y - size_factor*2/5 - gauge_size*.5, center_x + gauge_size*.4, bar_center_y - size_factor*2/5 - gauge_size*.5)

        painter.drawLine(center_x - gauge_size*.5, bar_center_y - size_factor*1/5 - gauge_size*.5, center_x + gauge_size*.5, bar_center_y - size_factor*1/5 - gauge_size*.5)
        painter.drawText(center_x - gauge_size*2, bar_center_y - size_factor*1/5, f"{int(self.max_value*3/5)}")

        painter.drawLine(center_x - gauge_size*.4, bar_center_y - gauge_size*.5, center_x + gauge_size*.4, bar_center_y - gauge_size*.5)

        painter.drawLine(center_x - gauge_size*.5, bar_center_y + size_factor*1/5 - gauge_size*.5, center_x + gauge_size*.5, bar_center_y + size_factor*1/5 - gauge_size*.5)
        painter.drawText(center_x - gauge_size*2, bar_center_y + size_factor*1/5, f"{int(self.max_value*2/5)}")

        painter.drawLine(center_x - gauge_size*.4, bar_center_y + size_factor*2/5 - gauge_size*.5, center_x + gauge_size*.4, bar_center_y + size_factor*2/5 - gauge_size*.5)

        painter.drawLine(center_x - gauge_size*.5, bar_center_y + size_factor*3/5 - gauge_size*.5, center_x + gauge_size*.5, bar_center_y + size_factor*3/5 - gauge_size*.5)
        painter.drawText(center_x - gauge_size*2, bar_center_y + size_factor*3/5, f"{int(self.max_value*1/5)}")

        painter.drawLine(center_x - gauge_size*.4, bar_center_y + size_factor*4/5 - gauge_size*.5, center_x + gauge_size*.4, bar_center_y + size_factor*4/5 - gauge_size*.5)

        painter.drawLine(center_x - gauge_size*.5, bar_center_y + size_factor*5/5 - gauge_size*.5, center_x + gauge_size*.5, bar_center_y + size_factor*5/5 - gauge_size*.5)
        painter.drawText(center_x - gauge_size*1.3, bar_center_y + size_factor*4.9/5, f"{0}")

        # Bottom Circle
        painter.setPen(QPen(QColor(Qt.green), gauge_size*4.5))
        painter.drawEllipse(center_x - gauge_size*.5, bar_center_y + size_factor*6/5, gauge_size,gauge_size)

        # Value Display
        painter.setPen(QPen(QColor(255, 255, 255)))
        Font = QFont("Baja", size_factor*.1)
        painter.setFont(Font)
        painter.drawText(center_x - gauge_size - size_factor*.02, bar_center_y + size_factor*6/5 + size_factor*.1, f"{self.value}")

        # Unit Display
        painter.setPen(QPen(QColor(255, 255, 255)))
        Font = QFont("Baja", size_factor*.15)
        painter.setFont(Font)
        painter.drawText(center_x - gauge_size*.5 + size_factor*.15, bar_center_y - size_factor + size_factor*.1, f"°C")



class Tachometer(QWidget):
    """
    @class Tachometer
    @brief A custom QWidget-based tachometer display widget.    

    This widget visually represents RPM (revolutions per minute) values using a combination of an arc and straight gauge bar.
    The gauge dynamically updates and fills using a gradient based on the current value.
    """

    def __init__(self, parent=None, max_value=5000):
        """
        @brief Constructor for the Tachometer widget.

        @param parent The parent widget (optional).
        @param max_value The maximum RPM value shown on the tachometer.
        """
        super().__init__(parent)
        self.value = 0  # Initial tachometer value
        self.max_value = max_value  # Maximum value of the tachometer
        self.setStyleSheet("background-color: black;")  # Set the background to black

        # USED IN PLACE OF OTHER 2 fonts (FONT: "Baja")
        font_id = QFontDatabase.addApplicationFont("Fonts/Baja.ttf")
        if font_id < 0: print("ERROR")
        font_families = QFontDatabase.applicationFontFamilies(font_id)


    def add_to_value(self, change):
        """
        @brief Add to the tachometer gauge value.

        @param change The add amount to change the current value by.
        The new value wraps around if it exceeds the max value.
        """
        # Update the tachometer value
        self.value = (self.value + change) % (self.max_value + 1)
        self.update()  # Request a redraw

    def update_value(self, new_value):
        """
        @brief Update the tachometer gauge value.

        @param new_value The new value for the gauge to be set to.
        The new value wraps around if it exceeds the max value.
        """
        # Update the tachometer value
        self.value = new_value % (self.max_value + 1)
        self.update()  # Request a redraw

    def paintEvent(self, event):
        """
        @brief Handle the paint event for rendering the gauge.

        This method draws the tachometer gauge, gradient fill, tick marks, and text labels.
        It also includes a half-circle and strait line and value/unit display. Also handles resizing.
        
        @param event The paint event triggered by Qt.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        size_factor = min(width, height) / 2 * 0.8
        


        # Draw the gauge arc and line (Grey backing)
        gauge_size = .1*size_factor
        painter.setPen(QPen(QColor(150,150,150), gauge_size))
        start_angle = 90
        span_angle = 90
        arc_rect = QRect(center_x - size_factor, center_y - size_factor, 2 * size_factor, 2 * size_factor)
        painter.drawArc(arc_rect, start_angle * 16, span_angle * 16)

        painter.drawLine(center_x, center_y - size_factor, center_x + size_factor, center_y - size_factor)


        # Gauge Gradient
        self.gaugeGrad = QLinearGradient(QPointF(center_x, center_y - size_factor), QPointF(center_x, center_y + size_factor))
        self.gaugeGrad.setColorAt(0, Qt.green)
        self.gaugeGrad.setColorAt(0.8, Qt.yellow)
        self.gaugeGrad.setColorAt(1, Qt.red)

        # Draw the value indicator 
        painter.setPen(QPen(self.gaugeGrad, gauge_size))

        # Arc section of Gauge Fill to value
        arc_start = 180
        arc_value = -1 * ((self.value / (self.max_value*.5)) * 90)
        if arc_value < -90:
            painter.drawArc(arc_rect, arc_start * 16, -90 * 16)
        else:
            painter.drawArc(arc_rect, arc_start * 16, arc_value * 16)

        # Line section of Gauge Fill to value

        if self.value > self.max_value*.5:
            length = (self.value - self.max_value*.5) / (self.max_value*.5) * size_factor
            painter.drawLine(center_x, center_y - size_factor, center_x + length, center_y - size_factor)


        # Draw the tick marks
        painter.setPen(QPen(QColor(255,255,255), 5))
        Font = QFont("Baja", size_factor*.05)
        painter.setFont(Font)

        # Flat line ticks

        # Last tick (MAX VALUE)
        painter.drawLine(center_x + size_factor + gauge_size*.5, center_y - size_factor - gauge_size*.5, center_x + size_factor + gauge_size*.5, center_y - size_factor + gauge_size*.5)
        painter.drawText(center_x + size_factor - gauge_size*.3, center_y - size_factor + gauge_size*1.4, f"{self.max_value}")

        painter.drawLine(center_x + size_factor*4/5 + gauge_size*.5, center_y - size_factor - gauge_size*.4, center_x + size_factor*4/5 + gauge_size*.5, center_y - size_factor + gauge_size*.4)

        painter.drawLine(center_x + size_factor*3/5 + gauge_size*.5, center_y - size_factor - gauge_size*.4, center_x + size_factor*3/5 + gauge_size*.5, center_y - size_factor + gauge_size*.4)
        painter.drawText(center_x + size_factor*3/5 - gauge_size*.3, center_y - size_factor + gauge_size*1.4, f"{int(self.max_value * 4/5)}")

        painter.drawLine(center_x + size_factor*2/5 + gauge_size*.5, center_y - size_factor - gauge_size*.4, center_x + size_factor*2/5 + gauge_size*.5, center_y - size_factor + gauge_size*.4)

        painter.drawLine(center_x + size_factor*1/5 + gauge_size*.5, center_y - size_factor - gauge_size*.4, center_x + size_factor*1/5 + gauge_size*.5, center_y - size_factor + gauge_size*.4)
        painter.drawText(center_x + size_factor*1/5 - gauge_size*.3, center_y - size_factor + gauge_size*1.4, f"{int(self.max_value * 3/5)}")
        
        # Half way tick
        painter.drawLine(center_x + gauge_size*.5, center_y - size_factor - gauge_size*.4, center_x + gauge_size*.5, center_y - size_factor + gauge_size*.4)

        # Curved ticks

        painter.drawLine(center_x - size_factor*90/360, center_y - size_factor*330/360, center_x - size_factor*97/360, center_y - size_factor*364/360)
        painter.drawText(center_x - size_factor*99/360 - gauge_size*.2, center_y - size_factor*330/360 + gauge_size*.9, f"{int(self.max_value * 2/5)}")
        
        painter.drawLine(center_x - size_factor*190/360, center_y - size_factor*288/360, center_x - size_factor*206/360, center_y - size_factor*312/360)
        
        painter.drawLine(center_x - size_factor*265/360, center_y - size_factor*216/360, center_x - size_factor*293/360, center_y - size_factor*238/360)
        painter.drawText(center_x - size_factor*265/360 + gauge_size*.3, center_y - size_factor*216/360 + gauge_size*.5, f"{int(self.max_value * 1/5)}")

        painter.drawLine(center_x - size_factor*323/360, center_y - size_factor*122/360, center_x - size_factor*352/360, center_y - size_factor*130/360)

        # First Tick (Value 0)
        painter.drawLine(center_x - size_factor + gauge_size*.5, center_y + gauge_size*.4, center_x - size_factor - gauge_size*.5, center_y + gauge_size*.4)
        painter.drawText(center_x - size_factor + gauge_size*.8, center_y + gauge_size*.5, f"{0}")

        # Draw the value text
        # painter.setPen(QPen(QColor(255, 255, 255)))
        # Font = QFont("7-Segment Classic", size_factor*.1)
        # painter.setFont(Font)
        # painter.drawText(center_x + size_factor*.4, center_y - size_factor - gauge_size*.9, f"{self.value}")
        # Font = QFont("Segment16C", size_factor*.125)
        # painter.setFont(Font)
        # painter.drawText(center_x + size_factor*.8, center_y - size_factor - gauge_size*.9, f"{"RPM"}")

        painter.setPen(QPen(QColor(255, 255, 255)))
        Font = QFont("Baja", size_factor*.1)
        painter.setFont(Font)
        painter.drawText(center_x + size_factor*.4, center_y - size_factor - gauge_size*.9, f"{self.value} RPM")
             

class Fuel_Gauge(QWidget):
    """
    @class Fuel_Gauge
    @brief A custom QWidget-based fuel gauge display widget.    

    This widget displays a circular fuel gauge that updates its display based on fuel level,
    including color-coded sections and tick marks.
    The percentage value of the current fuel is displayed inside the half-circle.
    """

    def __init__(self, parent=None, max_value=100):
        """
        @brief Constructor for the Fuel_Gauge widget.
        @param parent The parent widget (optional).
        @param max_value The maximum value the fuel gauge can represent.
        """
        super().__init__(parent)
        self.value = 0  # Initial Fuel Gauge value
        self.max_value = max_value  # Maximum value of the Fuel Gauge
        self.setStyleSheet("background-color: black;")  # Set the background to black

        # USED IN PLACE OF OTHER 2 fonts (FONT: "Baja")
        font_id = QFontDatabase.addApplicationFont("Fonts/Baja.ttf")
        if font_id < 0: print("ERROR")
        font_families = QFontDatabase.applicationFontFamilies(font_id)


    def add_to_value(self, change):
        """
        @brief Add to the fuel gauge value.

        @param change The add amount to change the current value by.
        The new value wraps around if it exceeds the max value.
        """
        # Update the Fuel Gauge value
        self.value = (self.value + change) % (self.max_value + 1)
        self.update()  # Request a redraw

    def update_value(self, new_value):
        """
        @brief Update the tachometer gauge value.

        @param new_value The new value for the gauge to be set to.
        The new value wraps around if it exceeds the max value.
        """
        # Update the Fuel Gauge value
        self.value = new_value % (self.max_value + 1)
        self.update()  # Request a redraw


    def paintEvent(self, event):
        """
        @brief Handle the paint event for rendering the gauge.

        This method draws the fuel gauge, gradient fill, tick marks, and text labels.
        It also includes a half-circle and and value/unit display. Also handles resizing.
        
        @param event The paint event triggered by Qt.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        size_factor = min(width, height) / 2 * 0.8

        # Draw the gauge arc
        start_angle = 170
        span_angle = 200
        painter.setPen(QPen(QColor(150, 150, 150), 15))
        painter.drawArc(center_x - size_factor, center_y - size_factor, 2 * size_factor, 2 * size_factor, start_angle * 16, span_angle * 16)

        # Draw the value indicator
        if self.value >= self.max_value*.4:
            painter.setPen(QPen(QColor(0, 255, 0), 15))
        elif self.value >= self.max_value*.2:
            painter.setPen(QPen(QColor(255, 255, 0), 15))
        elif self.value >= 0:
            painter.setPen(QPen(QColor(255, 0, 0), 15))
        else:
            painter.setPen(QPen(QColor(255, 0, 255), 15))

        arc_rect = QRect(center_x - size_factor, center_y - size_factor, 2 * size_factor, 2 * size_factor)

        arc_start = 170 # -370 deg
        arc_value = ((self.value / (self.max_value)) * 200)
        painter.drawArc(arc_rect, arc_start * 16, arc_value * 16)


        # Draw Tick marks (Each tick is 12.5% 8 ticks total unless the max value is not 100%)
        painter.setPen(QPen(QColor(255,255,255), 15))
        Font = QFont("Baja", size_factor*.2)
        painter.setFont(Font)
        
        painter.drawArc(arc_rect, 170*16, 1)
        painter.drawText(center_x - size_factor*320/360, center_y - size_factor*10/360, f"E")

        painter.drawArc(arc_rect, 195*16, 1)

        painter.drawArc(arc_rect, 220*16, 1)

        painter.drawArc(arc_rect, 245*16, 1)

        painter.drawArc(arc_rect, 270*16, 1)

        painter.drawArc(arc_rect, 295*16, 1)

        painter.drawArc(arc_rect, 320*16, 1)

        painter.drawArc(arc_rect, 345*16, 1)
    
        painter.drawArc(arc_rect, 10*16, 1)

        painter.drawText(center_x - size_factor*-280/360, center_y - size_factor*10/360, f"F")


        # FOR IF FUEL IS NOT TO BE PRINTED
        painter.setPen(QPen(QColor(255, 255, 255)))
        Font = QFont("Baja", size_factor*.25)
        painter.setFont(Font)
        painter.drawText(center_x - size_factor*90/360, center_y + size_factor*180/360, f"{int(self.value)}%")


class Speedometer(QWidget):
    """
    @class Speedometer
    @brief A QWidget-based speedometer that visually displays a numerical speed value in MPH.

    This widget presents a digital-style speedometer readout. The speed value is updated dynamically
    and rendered in a custom font, centered on the widget. The display adapts its text alignment
    based on the number of digits in the speed.
    """
    def __init__(self, parent=None, max_value=200):
        """
        @brief Constructor for the Speedometer widget.
        @param parent The parent widget (optional).
        @param max_value The maximum speed value that can be displayed.
        """
        super().__init__(parent)

        self.value = 0  # Initial speedometer value
        self.max_value = max_value  # Maximum value of the speedometer
        self.setStyleSheet("background-color: black;")

        # USED IN PLACE OF OTHER 2 fonts (FONT: "Baja")
        font_id = QFontDatabase.addApplicationFont("Fonts/Baja.ttf")
        if font_id < 0: print("ERROR")
        font_families = QFontDatabase.applicationFontFamilies(font_id)


    def add_to_value(self, change):
        """
        @brief Adds to the speedometer's value by a specified change.
        @param change The amount to adjust the current speed by. Wraps around on overflow.
        """
        # Update the speedometer value
        self.value = (self.value + change) % (self.max_value + 1)
        self.update()  # Request a redraw

    def update_value(self, new_value):
        """
        @brief Update the speedometer gauge value.

        @param new_value The new value for the gauge to be set to.
        The new value wraps around if it exceeds the max value.
        """
        # Update the speedometer value
        self.value = new_value % (self.max_value + 1)
        self.update()  # Request a redraw

    def paintEvent(self, event):
        """
        @brief Handle the paint event for rendering the speedometer.

        This method draws the speedometer, which is just a text label with RPM added to the end of it.
        
        @param event The paint event triggered by Qt.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        size_factor = min(width, height) / 2
        

        painter.setPen(QPen(QColor(255, 255, 255)))
        Font = QFont("Baja", size_factor*.25)
        painter.setFont(Font)

        if self.value >= 100:
            painter.drawText(center_x - size_factor*.5, center_y + size_factor*.25, f"{self.value}")
        elif self.value >= 10:
            painter.drawText(center_x - size_factor*.25, center_y + size_factor*.25, f"{self.value}")
        else:
            painter.drawText(center_x, center_y + size_factor*.25, f"{self.value}")

        painter.drawText(center_x - size_factor*.5 + size_factor*.75, center_y + size_factor*.25, f"MPH")


class Menu(QWidget):
    """
    @class Menu
    @brief A widget that displays a scrollable menu interface with selectable modes.

    The Menu widget provides a simple left-right navigable menu bar that appears at the bottom
    of the window. It takes the middle option as the currently selected mode and displays the previous and next 
    items in the menu list.
    """

    def __init__(self, parent=None, modes=[]):
        """
        @brief Constructor for the Menu widget.
        @param parent The parent widget (optional).
        @param modes A list of mode names to cycle through in the menu.
        """
        super().__init__(parent)
        # LAP TIME MIGHT NOT BE A VARIABLE SECTION AFTER COMPLETION ITEM COULD BE ALWAYS ACTIVE
        self.modes = modes
        self.num_of_modes = len(self.modes)
        self.state = "Startup" # Initial Menu value

        self.setStyleSheet("background-color: black;")

        # USED IN PLACE OF OTHER 2 fonts (FONT: "Baja")
        font_id = QFontDatabase.addApplicationFont("Fonts/Baja.ttf")
        if font_id < 0: print("ERROR")
        font_families = QFontDatabase.applicationFontFamilies(font_id)


    def update_value(self, move_value):
        """
        @brief Updates the currently selected menu state.
        @param move_value The number of steps to move in the modes list (positive or negative).
        """
        # Change the menu's mode
        if (self.modes.index(self.state) + move_value) < self.num_of_modes:
            self.state = self.modes[self.modes.index(self.state) + move_value]
        else:
            self.state = self.modes[0]

        self.update()  # Request a redraw


    def paintEvent(self, event):
        """
        @brief Paint event handler that draws the menu bar and its current state.
        @param event The QPaintEvent that triggered the paint update.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(0, 0, 0), 10))

        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = 14/15*height / 2 # Half way in the rectangle of the menu not the center of the window
        size_factor = min(width, height) / 2 * 0.8

        menu_background = QRect(0, 14/15*height, width, height/15)
        painter.fillRect(menu_background, QBrush(QColor(255, 255, 255)))


        left_item = QRect(0, 14/15*height, width/3, height/15)
        selected_item = QRect(width/3, 14/15*height, width/3, height/15)
        right_item = QRect(width*2/3, 14/15*height, width/3, height/15)

        painter.setFont(QFont("Sans Sariff", size_factor/10, QFont.Bold))
        painter.drawText(selected_item, Qt.AlignCenter, f"{self.state}")

        painter.drawText(left_item, Qt.AlignCenter, f"{self.modes[self.modes.index(self.state) - 1]}")

        if (self.modes.index(self.state) + 1) < self.num_of_modes:
            painter.drawText(right_item, Qt.AlignCenter, f"{self.modes[self.modes.index(self.state) + 1]}")
        else:
            painter.drawText(right_item, Qt.AlignCenter, f"{self.modes[0]}")




class Rotating_Image(QWidget):
    """
    @class Rotating_Image
    @brief A QWidget that cycles through a list of PNG images at a set interval.

    The Rotating_Image widget displays one image at a time from a provided list of PNG paths.
    It automatically rotates to the next image after a fixed time interval. The displayed image
    resizes dynamically with the widget while maintaining its aspect ratio.
    """
    def __init__(self, parent=None, png_paths=[], height=100, width=100, image_time=10000):
        """
        @brief Constructor for the Rotating_Image widget.
        @param parent The parent widget (optional).
        @param png_paths List of file paths to PNG images for rotation.
        @param height Initial height of the image display area.
        @param width Initial width of the image display area.
        @param image_time The length of time in milliseconds that a image is displayed before it changes.
        """
        super().__init__(parent)
        self.setStyleSheet("background-color: black;")
        self.png_paths = png_paths
        self.num_of_paths = len(png_paths)
        self.current_path = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_image)
        self.timer.start(image_time)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)

        # Load the pixmap only if the path is valid
        if self.png_paths[self.current_path]:
            pixmap = QPixmap(self.png_paths[self.current_path])
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)



    def resizeEvent(self, event):
        """
        @brief Handles widget resizing and scales the image accordingly.
        @param event QResizeEvent triggered when the widget is resized.
        """
        super().resizeEvent(event)
        self.label.setGeometry(self.rect())  # Make the label fill the entire widget

        # Resize the pixmap to fit the label while maintaining the aspect ratio
        if self.label.pixmap():
            self.label.setPixmap(self.label.pixmap().scaled(self.label.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))


    def change_image(self):
        """
        @brief Advances to the next image in the list and updates the display.
        
        This method is called automatically by a timer. It cycles through the image list
        and applies scaling to fit the widget's dimensions.
        """
        next_image = (self.current_path + 1) % self.num_of_paths
        new_pixmap = self.png_paths[next_image]
        self.current_path += 1
        if self.png_paths[next_image]:
            pixmap = QPixmap(self.png_paths[next_image])
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

        if self.label.pixmap():
            self.label.setPixmap(self.label.pixmap().scaled(self.label.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))







class Variable_Section(QWidget):
    """
    @class Variable_Section
    @brief A QWidget that handles a wide variety of uses for the Bobcat Baja team.*Bold* Not recommend to use as is outside of Bobcat Baja.

    A set of custom widgets that have specific uses for Bobcat Baja.
    These currently include "Startup", "Competition", "Rear Steer", "Two-Step" and "Lap Time" although they are not all complete.
    """
    def __init__(self, parent=None):
        """
        @brief Constructor for the variable section widget. Initializes to "Startup" sub-widget.
        @param parent The parent widget (optional).
        """
        super().__init__(parent)
        self.setStyleSheet("background-color: black;")

        # FONT: "Baja"
        font_id = QFontDatabase.addApplicationFont("Fonts/Baja.ttf")
        if font_id < 0: print("ERROR")
        font_families = QFontDatabase.applicationFontFamilies(font_id)


        self.widget_types = ["Startup", "Competition", "Rear Steer", "Two-Step", "Lap Time"]

        # Startup will display a text box that explains how to use the HID and switch for the diffs
        self.current_widget = "Startup"

        # Vars for 2 step function
        self.new_two_step_bounds = [0,0]
        self.two_step_digit_list = ["first_digit", "second_digit", "third_digit", "forth_digit", "rmp_digit"]
        self.selected_two_step_digit = "first_digit"
        self.two_step_bound = "Upper"
        self.two_step_current_digit_values = [0,0,0,0]
        self.two_step_value_up = True
        self.two_step_bad_input = False

    def change_widget(self, new_widget):
        """
        @brief Changes the variable section to the new widget that is passed to it and redraws the new widget.
        @param new_widget The new widget to be displayed.
        """
        self.current_widget = new_widget

        # Default vars used for 2 step
        if new_widget == "Two-Step":
            self.new_two_step_bounds = [0,0]
            self.selected_two_step_digit = "first_digit"
            self.two_step_bound = "Upper"
            self.two_step_current_digit_values = [0,0,0,0]
            self.two_step_value_up = True
            self.two_step_bad_input = False

        self.update()  # Request a redraw

    def paintEvent(self, event):
        """
        @brief Paint event handler that calls the function that the variable widget is set to by its current state.
        @param event The QPaintEvent that triggered the paint update.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        self.size_factor = min(width, height) / 2 * 0.8
        
        
        if (self.current_widget == "Startup"):
            self.draw_Startup(painter)

        elif (self.current_widget == "Competition"):
            None

        elif (self.current_widget == "Rear Steer"):
            None

        elif (self.current_widget == "Two-Step"):
            self.draw_Two_Step(painter)

        elif (self.current_widget == "Lap Time"):
            None

        else:
            self.draw_Error(painter)


    def draw_Startup(self, painter):
        """
        @brief Draws the startup instructional overlay on the widget.
        @param painter QPainter object used for rendering text on the widget.

        This function displays startup instructions for both the HID Control and Switch Control systems.
        It sets the pen and font style, defines the drawing rectangle, and renders a multiline instructional
        string aligned to the top-left of the widget using word wrapping.
        """
        painter.setPen(QPen(QColor(255, 255, 255)))
        Font = QFont("Sans Sariff", self.size_factor/13, QFont.Bold)
        painter.setFont(Font)
        
        widget_rect = QRect(0, 0, self.width(), self.height())
        startup_string = f"""HID Control Manual: 
    The center button will pull up a menu in the bottom of the dash that can be navigated using the left and right buttons. 
    When the option you want is in the center slot of the 3 shown press the middle/select button to change the variable section (this one).
    For the Two-step controls use the top and bottom buttons to increment or decrement the highlighted digit and use left and right to select another digit.
    After the values are set correctly press the middle button to set the values and ... (Return to competition widget?)
        
Switch Control Manual:
    Open: Green
    Semi: Blue
    Locked: Red
"""
        painter.drawText(widget_rect, Qt.TextWordWrap | Qt.AlignLeft | Qt.AlignTop, startup_string)

    #TODO
    def draw_Competition(self, painter):
        """
        @brief Draws the Competition overlay on the widget.
        @param painter QPainter object used for rendering text on the widget.

        This function is not complete.
        """
        None

    
    def draw_Rear_Steer(self, painter):
        """
        @brief Draws the Rear Steer overlay on the widget.
        @param painter QPainter object used for rendering text on the widget.

        This function is not complete.
        """
        None
    
    
    def draw_Two_Step(self, painter):
        """
        @brief Draws the two-Step RPM limit adjustment interface.
        @param painter QPainter object used to render the visual interface.

        This function draws the two-step RPM bounds adjustment screen, which allows the user to configure
        both the upper or lower RPM limits using four editable digits. A title is displayed to indicate
        the bound currently being edited, and if bad input was previously received, an error message is shown instead.
        Each digit is visually represented, with one digit highlighted to indicate the current selection.
        """
        # Background Color
        painter.setPen(QPen(QColor(255, 255, 255), 15))
        widget_rect = QRect(0, 0, self.width(), self.height())
        painter.fillRect(widget_rect, QBrush(QColor(200, 200, 200)))

        widget_rect = QRect(0, self.size_factor*.5, self.width(), self.height()-self.size_factor*.5)
        painter.fillRect(widget_rect, QBrush(QColor(255, 255, 255)))

        # Title
        painter.setPen(QPen(QColor(0, 0, 0), 15))

        #CHECK IF BAD INPUT WAS PUT IN LAST
        if self.two_step_bad_input:
            Font = QFont("Sans Sariff", self.size_factor*.1, QFont.Bold)
            painter.setFont(Font)
            painter.drawText(QRect(0, 0, self.width(), self.size_factor*.5), "BAD BOUNDS REOPEN FROM MENU", Qt.AlignCenter)
        else:
            Font = QFont("Sans Sariff", self.size_factor*.15, QFont.Bold)
            painter.setFont(Font)
            if self.two_step_bound == "Upper":
                painter.drawText(QRect(0, 0, self.width(), self.size_factor*.5), "Upper 2-Step Bound", Qt.AlignCenter)
            elif self.two_step_bound == "Lower":
                painter.drawText(QRect(0, 0, self.width(), self.size_factor*.5), "Lower 2-Step Bound", Qt.AlignCenter)
            else:
                print("ERROR BAD 2 Step Bound")

        # 1st digit
        first_digit_rect = QRect(0, self.size_factor*.5, self.width()/5, self.height()-self.size_factor*.5)
        # painter.fillRect(widget_rect, QBrush(QColor(0, 255, 255)))
        

        # 2nd digit
        second_digit_rect = QRect(self.width()/5, self.size_factor*.5, self.width()/5, self.height()-self.size_factor*.5)
        # painter.fillRect(widget_rect, QBrush(QColor(255, 0, 255)))

        # 3rd digit
        third_digit_rect = QRect(self.width()/5*2, self.size_factor*.5, self.width()/5, self.height()-self.size_factor*.5)
        # painter.fillRect(widget_rect, QBrush(QColor(255, 255, 0)))

        # 4th digit
        forth_digit_rect = QRect(self.width()/5*3, self.size_factor*.5, self.width()/5, self.height()-self.size_factor*.5)
        # painter.fillRect(widget_rect, QBrush(QColor(0, 0, 255)))

        # RPM label
        rmp_digit_rect = QRect(self.width()/5*4, self.size_factor*.5, self.width()/5, self.height()-self.size_factor*.5)
        painter.setPen(QPen(QColor(0, 0, 0), 15))
        Font = QFont("Baja", self.size_factor*.2, QFont.Bold)
        painter.setFont(Font)
        painter.drawText(rmp_digit_rect, "RPM", Qt.AlignCenter)


        # Draw the indicator for which digit is being edited/changed
        painter.setPen(QPen(QColor(0, 0, 0), self.size_factor*.05))

        match (self.selected_two_step_digit):
            case "first_digit":
                painter.drawRect(first_digit_rect)
            case "second_digit":
                painter.drawRect(second_digit_rect)
            case "third_digit":
                painter.drawRect(third_digit_rect)
            case "forth_digit":
                painter.drawRect(forth_digit_rect)
            case "rmp_digit":
                painter.drawRect(rmp_digit_rect)
            case _:
                print("BAD INDEX ON 2 STEP SELECTOR")

        # Draw the current digits for the bounds
        Font = QFont("Baja", self.size_factor*.4, QFont.Bold)
        painter.setFont(Font)

        painter.drawText(first_digit_rect, str(self.two_step_current_digit_values[0]), Qt.AlignCenter)
        painter.drawText(second_digit_rect, str(self.two_step_current_digit_values[1]), Qt.AlignCenter)
        painter.drawText(third_digit_rect, str(self.two_step_current_digit_values[2]), Qt.AlignCenter)
        painter.drawText(forth_digit_rect, str(self.two_step_current_digit_values[3]), Qt.AlignCenter)



    def update_two_step(self, value):
        """
        @brief Updates the currently selected two-step digit by a given increment or decrement.
        @param value Integer value to apply (+1 to increment, -1 to decrement the selected digit).

        This function modifies one of the four digit values used for setting the two-step RPM limit,
        depending on which digit is currently selected. Each digit is constrained between 0-9 by modding by 10.
        The function then requests a repaint of the widget to reflect the updated value.
        """
        match (self.selected_two_step_digit):
            case "first_digit":
                # inc or dec the self.two_step_current_digit_values[0] value by 1 then % 10
                self.two_step_current_digit_values[0] = (self.two_step_current_digit_values[0] + value) % 10

            case "second_digit":
                # inc or dec the self.two_step_current_digit_values[1] value by 1 then % 10
                self.two_step_current_digit_values[1] = (self.two_step_current_digit_values[1] + value) % 10

            case "third_digit":
                # inc or dec the self.two_step_current_digit_values[2] value by 1 then % 10
                self.two_step_current_digit_values[2] = (self.two_step_current_digit_values[2] + value) % 10

            case "forth_digit":
                # inc or dec the self.two_step_current_digit_values[3] value by 1 then % 10
                self.two_step_current_digit_values[3] = (self.two_step_current_digit_values[3] + value) % 10

            case "rmp_digit":
                None
            case _:
                print("BAD INDEX ON 2 STEP SELECTOR")

        self.update()

    def move_two_step(self):
        """
        @brief Handles the progression through the two-step digit selection and boundary-setting process.

        If the currently selected digit is the RPM label (end of the sequence), then:
        - If setting the "Upper" bound, the digit values are converted into an integer and saved as the upper limit.
        - If setting the "Lower" bound, the digit values are saved as the lower limit. If the lower limit is not less than the upper,
          a flag is raised to show bad input. Otherwise, a transition to the Competition widget is triggered.
        
        If the current selection is not the RPM digit, moves selection to the next digit in the digit list.

        Always triggers a repaint of the widget to reflect current state.
        """
        # if it is at the RPM digit
        if self.selected_two_step_digit == "rmp_digit":
                # Update the self.two_step_bound to "Lower" if it is "Upper" or send the values over canbus if it is already "Lower"
                if self.two_step_bound == "Upper":
                    self.new_two_step_bounds[0] = self.two_step_current_digit_values[0]*1000 + self.two_step_current_digit_values[1]*100 + self.two_step_current_digit_values[2]*10 + self.two_step_current_digit_values[3]
                    self.two_step_bound = "Lower"
                    self.two_step_current_digit_values = [0,0,0,0]
                    self.selected_two_step_digit = "first_digit"

                elif self.two_step_bound == "Lower":
                    self.new_two_step_bounds[1] = self.two_step_current_digit_values[0]*1000 + self.two_step_current_digit_values[1]*100 + self.two_step_current_digit_values[2]*10 + self.two_step_current_digit_values[3]
                    
                    if self.new_two_step_bounds[1] >= self.new_two_step_bounds[0]:
                        self.two_step_bad_input = True
                        
                    else:
                        # Replace this line with CANBUS SEND OR MAYBE IN DASH CODE TODO RETURN TOUPLE OF INTS TO LET DASH CODE HANDLE IT
                        self.change_widget("Competition")
                        print("TWO STEP BOUNDS ARE: ", self.new_two_step_bounds)
                else:
                    print("ERROR BAD self.two_step_bound")
            
        else:
            self.selected_two_step_digit = self.two_step_digit_list[self.two_step_digit_list.index(self.selected_two_step_digit) + 1]

        self.update()

    def draw_Lap_Time(self, painter):
        """
        @brief Draws the Lap Time overlay on the widget.
        @param painter QPainter object used for rendering text on the widget.

        This function is not complete.
        """
        None


    def draw_Error(self, painter):
        """
        @brief Draws the Error overlay on the widget.
        @param painter QPainter object used for rendering text on the widget.

        This function only occurs when the widget selected doesn't have a draw function for it.
        """
        painter.setPen(QPen(QColor(255, 255, 255)))
        Font = QFont("Sans Sariff", self.size_factor/12, QFont.Bold)
        painter.setFont(Font)
        
        widget_rect = QRect(0, 0, self.width(), self.height())
        error_string = f"ERROR WITH VARIABLE WIDGET. PLEASE HELP! :("

        painter.drawText(widget_rect, Qt.TextWordWrap | Qt.AlignLeft | Qt.AlignTop, error_string)


