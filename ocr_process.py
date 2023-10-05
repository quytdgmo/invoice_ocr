import os
from typing import Optional, Sequence
from google.api_core.client_options import ClientOptions
from google.cloud import documentai

class InvoiceOCR(object):  

    def __init__( self ):
        self.name = 'InvoiceOCR'
        self.project_id =os.environ.get("PROJECT_ID")
        self.location = os.environ.get("PROCESSOR_LOCATION") 
        self.processor_id = os.environ.get("PROCESSOR_ID")  
        self.processor_version = os.environ.get("PROCESS_VERSION")

    def process_invoice_ocr(
        self,
        file_path: str,
        mime_type: str,
    ) -> documentai.Document:
        # Online processing request to Document AI
        document = self.process_document(
            self.project_id, self.location, self.processor_id, self.processor_version, file_path, mime_type
        )

        # Read the table and form fields output from the processor
        # The form processor also contains OCR data. For more information
        # on how to parse OCR data please see the OCR sample.

        text = document.text
        print(f"Full document text: {repr(text)}\n")
        
        ocr_result = ""

        # Read the form fields and tables output from the processor
        for page in document.pages:
            print(f"\n\n**** Page {page.page_number} ****")

            print(f"\nFound {len(page.tables)} table(s):")
            for table in page.tables:
                num_columns = len(table.header_rows[0].cells)
                num_rows = len(table.body_rows)
                print(f"Table with {num_columns} columns and {num_rows} rows:")

                # Print header rows
                #print("Columns:")
                header_data = self.print_table_rows(table.header_rows, text)
                ocr_result += header_data + "\n"

                # Print body rows
                #print("Table body data:")
                table_data = self.print_table_rows(table.body_rows, text)
                ocr_result += table_data + "\n"

            print(f"\nFound {len(page.form_fields)} form field(s):")
            for field in page.form_fields:
                name = self.layout_to_text(field.field_name, text)
                value = self.layout_to_text(field.field_value, text)
                form_data = f"    * {repr(name.strip())}: {repr(value.strip())}"
                ocr_result += form_data + "\n"

        return ocr_result


    def print_table_rows(
        self,
        table_rows: Sequence[documentai.Document.Page.Table.TableRow], text: str
    ) -> str:
        result = ""
        for table_row in table_rows:
            row_text = ""
            for cell in table_row.cells:
                cell_text = self.layout_to_text(cell.layout, text)
                row_text += f"{repr(cell_text.strip())} | "
            result += row_text + "\n"
        
        return result 

    def process_document(
        self,
        project_id: str,
        location: str,
        processor_id: str,
        processor_version: str,
        file_path: str,
        mime_type: str,
        process_options: Optional[documentai.ProcessOptions] = None,
    ) -> documentai.Document:
        # You must set the `api_endpoint` if you use a location other than "us".
        client = documentai.DocumentProcessorServiceClient(
            client_options=ClientOptions(
                api_endpoint=f"{location}-documentai.googleapis.com"
            )
        )

        # The full resource name of the processor version, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
        # You must create a processor before running this sample.
        name = client.processor_version_path(
            project_id, location, processor_id, processor_version
        )

        # Read the file into memory
        with open(file_path, "rb") as image:
            image_content = image.read()

        # Configure the process request
        request = documentai.ProcessRequest(
            name=name,
            raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
            # Only supported for Document OCR processor
            process_options=process_options,
        )

        result = client.process_document(request=request)

        # For a full list of `Document` object attributes, reference this page:
        # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
        return result.document


    def layout_to_text(self, layout: documentai.Document.Page.Layout, text: str) -> str:
        """
        Document AI identifies text in different parts of the document by their
        offsets in the entirety of the document"s text. This function converts
        offsets to a string.
        """
        # If a text segment spans several lines, it will
        # be stored in different text segments.
        return "".join(
            text[int(segment.start_index) : int(segment.end_index)]
            for segment in layout.text_anchor.text_segments
        )





