from PIL import Image as PIL_IMAGE
from borb.pdf.canvas.color.color import X11Color
from pathlib import Path
from borb.pdf.canvas.color.color import X11Color


from decimal import Decimal
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable 



from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.table import TableCell

from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import DestinationType, Page
from borb.pdf.page.page_size import PageSize
from borb.pdf.pdf import PDF
from borb.pdf.canvas.layout.image.image import Image  as Image_Borb
import numpy as np


def printPdf(data, graph, specgram):

        print("----------------------")
        print(len(data))
        print(data)
        doc: Document = Document()

        page: Page = Page(PageSize.A4_LANDSCAPE.value[0], PageSize.A4_LANDSCAPE.value[0])
        doc.append_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        p: Paragraph = Paragraph("Signal Report",font_color = X11Color("Red"), horizontal_alignment=Alignment.CENTERED,font = "Helvetica_bold",font_size = 20)
        layout.add(p)
        if len(data) ==3:

            layout.add(
                FixedColumnWidthTable(number_of_columns=5, number_of_rows=4,horizontal_alignment=Alignment.CENTERED)
                # row 1
                .add(
                    TableCell(
                        Paragraph(" "),
                    )
                )
                .add(Paragraph("Mean", text_alignment=Alignment.CENTERED))
                .add(Paragraph("STD", text_alignment=Alignment.CENTERED))
                .add(Paragraph("Min", text_alignment=Alignment.CENTERED))
                .add(Paragraph("Max", text_alignment=Alignment.CENTERED))

                # row 2
                .add(Paragraph("ECG Signal"),)
                .add(Paragraph(str(data[0][0]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[0][1]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[0][2]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[0][3]),text_alignment=Alignment.CENTERED))
                # row 3
                .add(Paragraph("EMG Signal"),)
                .add(Paragraph(str(data[1][0]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[1][1]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[1][2]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[1][3]),text_alignment=Alignment.CENTERED))

                # row 4
                .add(Paragraph("EOG Signal"),)
                .add(Paragraph(str(data[2][0]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[2][1]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[2][2]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[2][3]),text_alignment=Alignment.CENTERED))

                .set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
                .even_odd_row_colors(X11Color("LightGray"), X11Color("White"))
                .no_borders()
        )
        elif len(data) == 4:
            layout.add(
                FixedColumnWidthTable(number_of_columns=5, number_of_rows=2,horizontal_alignment=Alignment.CENTERED)

                .add(
                    TableCell(
                        Paragraph(" "),
                    )
                )
                .add(Paragraph("Mean", text_alignment=Alignment.CENTERED))
                .add(Paragraph("STD ", text_alignment=Alignment.CENTERED))
                .add(Paragraph("Min ", text_alignment=Alignment.CENTERED))
                .add(Paragraph("Max ", text_alignment=Alignment.CENTERED))

                # row 2
                .add(Paragraph(("ECG Signal"),text_alignment=Alignment.CENTERED),)
                .add(Paragraph(str(data[0][0]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[0][1]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[0][2]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[0][3]),text_alignment=Alignment.CENTERED))

                .set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
                .even_odd_row_colors(X11Color("LightGray"), X11Color("White"))
                .no_borders()
            )

        elif len(data) ==2:

            layout.add(
                FixedColumnWidthTable(number_of_columns=5, number_of_rows=3,horizontal_alignment=Alignment.CENTERED)
                # row 1
                .add(
                    TableCell(
                        Paragraph(" "),
                    )
                )
                .add(Paragraph("Mean", text_alignment=Alignment.CENTERED,))
                .add(Paragraph("STD", text_alignment=Alignment.CENTERED))
                .add(Paragraph("Min", text_alignment=Alignment.CENTERED))
                .add(Paragraph("Max", text_alignment=Alignment.CENTERED))

                # row 2
                .add(Paragraph("ECG Signal",text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[0][0]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[0][1]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[0][2]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[0][3]),text_alignment=Alignment.CENTERED))
                # row 3
                .add(Paragraph("ECG Signal",text_alignment=Alignment.CENTERED,))
                .add(Paragraph(str(data[1][0]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[1][1]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[1][2]),text_alignment=Alignment.CENTERED))
                .add(Paragraph(str(data[1][3]),text_alignment=Alignment.CENTERED))

                .set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
                .even_odd_row_colors(X11Color("LightGray"), X11Color("White"))
                .no_borders()
        )
        # PIL_Iage = Image.fromarray(X[0].astype('uint8'), 'RGB')
        layout.add(Paragraph(" "))
        layout.add(Image_Borb(graph,  width=Decimal(512),  height=Decimal(240)))
        layout.add(Image_Borb(specgram,  width=Decimal(512),  height=Decimal(240)))

        if len(data) == 3:
            layout.add(Paragraph("Channel 1", horizontal_alignment=Alignment.CENTERED,font = "Helvetica_bold",font_size = 15))   

        elif len(data) == 2:
            layout.add(Paragraph("Channel 2", horizontal_alignment=Alignment.CENTERED,font = "Helvetica_bold",font_size = 15))  

        elif len(data) == 1:
            layout.add(Paragraph("Channel 3", horizontal_alignment=Alignment.CENTERED,font = "Helvetica_bold",font_size = 15)) 



        with open("output.pdf", "wb") as out_file_handle:
                PDF.dumps(out_file_handle, doc)   

