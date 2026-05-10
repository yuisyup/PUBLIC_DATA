import { CsvUploadForm } from "../components/form/CsvUploadForm";

export function CsvUploadPage() {
    return (
        <div>
            <div className="bg-primary text-white p-3 mb-4">
                <h3 className="text-white">CSV読み込み</h3>
            </div>

            <CsvUploadForm />
        </div>
    );
}