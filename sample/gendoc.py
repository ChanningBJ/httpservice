from httpservice.DocGenerator import DocGenerator
import app

if __name__ == '__main__':
    doc_generator = DocGenerator('doc','doc_html')
    doc_generator.add_service(app.SampleService)
    doc_generator.generate_doc()