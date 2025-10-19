import pandas as pd
from pathlib import Path
from typing import Tuple, List, Union
import chardet

class MultiFileReader:
    """
    Загружает данные Энергия, Дж и Длительность сигнала, мс в X и Y из файлов TXT, CSV и Excel.
    """
    
    SUPPORTED_EXTENSIONS = {".txt", ".csv", ".xls", ".xlsx"}
    
    def load(self, file_path: Union[str, Path]) -> Tuple[List[float], List[float]]:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        ext = file_path.suffix.lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Неподдерживаемый формат файла: {ext}")
        
        df = self._read_file(file_path, ext)
        
        # Извлекаем нужные колонки
        if "Энергия, Дж" not in df.columns or "Длительность сигнала, мс" not in df.columns:
            raise KeyError("В файле нет нужных данных")
        
        x_series = df["Энергия, Дж"].astype(str).str.replace(',', '.')
        y_series = df["Длительность сигнала, мс"].astype(str).str.replace(',', '.')
        
        X = pd.to_numeric(x_series, errors='coerce').dropna().tolist()
        Y = pd.to_numeric(y_series, errors='coerce').dropna().tolist()
        
        return X, Y

    @staticmethod
    def _read_file(file_path: Path, ext: str) -> pd.DataFrame:
        if ext in {".csv", ".txt"}:
            # Сначала определяем кодировку файла
            with open(file_path, "rb") as f:
                rawdata = f.read()
                result = chardet.detect(rawdata)
                encoding = result['encoding']
            
            return pd.read_csv(file_path, sep=None, engine="python", decimal=',', encoding=encoding)
        
        elif ext in {".xls", ".xlsx"}:
            return pd.read_excel(file_path)
        
        else:
            raise ValueError(f"Неизвестный тип файла: {ext}")

