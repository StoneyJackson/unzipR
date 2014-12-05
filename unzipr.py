#   unzipR - A library for recursively extracting files.
#   Copyright (C) 2014  Stoney Jackson <dr.stoney@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''
Unzipr determines a files compression algorithm based on the file's
extension.  Zip files are extracted into the a directory by the same name as
the zip file minus its extension. So foo.zip is extracted in to a directory
named foo.

New formats can be supports via Unzipr.registerUnzipFormat().
See installRarSupport() at the end of this file for an example.
'''


import pathlib
import shutil
import logging
logger = logging.getLogger(__name__)


def deleteZipFilesFromDirectoryRecursively(directory):
    directory = pathlib.Path(directory)
    for a_file in directory.iterdir():
        if isZipFile(a_file):
            a_file.unlink()
        elif a_file.is_dir():
            deleteZipFilesFromDirectoryRecursively(a_file)

def unzipFileRecursively(zipfile, toDir=None):
    '''
    If toDir is None, zipfile is extracted to a directory whose name is the same
    as the zipfile's name minus its extensions.
    '''
    zipfile = pathlib.Path(zipfile)
    toDir = unzipFile(zipfile, toDir)
    unzipFilesInDirectoryRecursively(toDir)
    return toDir

def unzipFilesInDirectoryRecursively(directory):
    directory = pathlib.Path(directory)
    for a_file in directory.iterdir():
        logger.debug("processing " + str(a_file))
        if isZipFile(a_file):
            logger.debug("unzipping " + str(a_file))
            unzipFileRecursively(a_file)
        elif a_file.is_dir():
            logger.debug("recursing " + str(a_file))
            unzipFilesInDirectoryRecursively(a_file)

def unzipFile(zipfile, toDir=None):
    '''
    If toDir is None, zipfile is extracted to a directory whose name is the same
    as the zipfile's name minus its extensions.
    '''
    zipfile = pathlib.Path(zipfile)
    if toDir:
        toDir = pathlib.Path(toDir)
    else:
        toDir = zipfile.parent / getFileNameWithoutExtension(zipfile)
    shutil.unpack_archive(str(zipfile), str(toDir))
    return toDir

def getFileNameWithoutExtension(theFile):
    theFile = pathlib.Path(theFile)
    extension = getFileExtension(theFile)
    return theFile.name[:-len(extension)]

def isZipFile(zipfile):
    zipfile = pathlib.Path(zipfile)
    isZipFile = zipfile.is_file() and fileHasSupportedExtension(zipfile)
    return isZipFile

def fileHasSupportedExtension(zipfile):
    zipfile = pathlib.Path(zipfile)
    extension = getFileExtension(zipfile)
    return isSupportedExtension(extension)

def getFileExtension(theFile):
    if len(theFile.suffixes) >= 2:
        lastTwoSuffixes = ''.join(theFile.suffixes[-2:])
        if lastTwoSuffixes == '.tar.gz':
            return lastTwoSuffixes
    else:
        return theFile.suffix

def isSupportedExtension(extension):
    return extension in getSupportedExtensions()

def getSupportedExtensions():
    supported_extensions = []
    for format_ in shutil.get_unpack_formats():
        supported_extensions += format_[1]
    return supported_extensions

def registerUnzipFormat(name, extensions, function):
    shutil.register_unpack_format(name, extensions, function)

def installRarSupport():
    try:
        import rarfile

        def unrar(zipFile, toDir):
            with rarfile.RarFile(zipFile) as rf:
                rf.extractall(path=toDir)
    
        registerUnzipFormat('rar', ['.rar'], unrar)
    except ImportError:
        pass


def install7zipSupport():
    if shutil.which('7z'):
        import subprocess

        def un7zip(zipFile, toDir):
            subprocess.call(['7z', 'x', str(zipFile), '-o' + str(toDir)])

        registerUnzipFormat('7zip', ['.7z'], un7zip)


installRarSupport()
install7zipSupport()
