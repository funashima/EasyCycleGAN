#!/usr/bin/env python3
import urllib.request
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import shutil


class DLBaseKit(object):
    def __init__(self) -> None:
        self.pbar = None
        self.ucb_url = "http://efrosgans.eecs.berkeley.edu/cyclegan/"
        self.last_block_count = 0

    def _get_file_list(self, filetype: str = "") -> list:
        if filetype in ['datasets', 'pretrained_models']:
            url = urllib.parse.urljoin(self.ucb_url, filetype)
        else:
            print('===== Error ====')
            print(f'filetype {filetype} is undefined')
            exit()
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        file_list = []
        for a in soup.find_all('a'):
            href = a.get('href')
            suffix = self._get_suffix(filetype=filetype)
            if href and href.endswith(suffix):
                file_list.append(href)
        return file_list

    def _get_suffix(self, filetype: str = "") -> str:
        if filetype == 'datasets':
            suffix = '.zip'
        elif filetype == 'pretrained_models':
            suffix = '.pth'
        return suffix

    def _download(self, filetype: str = "", keyword: str = "") -> None:
        target = [os.path.splitext(x)[0] for x in
                  self._get_file_list(filetype=filetype)]
        if keyword in target:
            suffix = self._get_suffix(filetype=filetype)
            filename = keyword + suffix
            url = urllib.parse.urljoin(urllib.parse.urljoin(self.ucb_url,
                                                            filetype+'/'),
                                       filename)
            urllib.request.urlretrieve(url, filename, self._progress)

    def _progress(self, block_count: int, block_size: int, total_size: int):
        if self.pbar is None:
            self.pbar = tqdm(total=total_size)
        delta = (block_count - self.last_block_count) * block_size
        self.pbar.update(delta)
        self.last_block_count = block_count
        if block_count * block_size >= total_size:
            self.pbar.close()
            self.pbar = None

    def postprocess(self) -> None:
        pass


class DLDatasets(DLBaseKit):
    def __init__(self) -> None:
        super().__init__()
        self.filetype = 'datasets'

    def get_file_list(self) -> None:
        self._get_file_list(filetype=self.filetype)

    def download(self, keyword: str = "") -> None:
        self._download(filetype=self.filetype, keyword=keyword)

    def get_suffix(self) -> str:
        self._get_suffix(filetype=self.filetype)


class DLPretrainedModels(DLBaseKit):
    def __init__(self):
        super().__init__()
        self.filetype = 'pretrained_models'

    def get_file_list(self) -> None:
        self._get_file_list(filetype=self.filetype)

    def download(self, keyword: str = "") -> None:
        self._download(filetype=self.filetype, keyword=keyword)

    def get_suffix(self) -> str:
        self._get_suffix(filetype=self.filetype)

    def postprocess(self, keyword: str = "", filename="") -> None:
        pass

        


# Usage example:
if __name__ == '__main__':
    dld = DLPretrainedModels()
    dld.download(keyword='apple2orange')
