import os
import sass
import shutil

class AssetCompiler(object):
  def __init__(self):
    self.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    self.sass_src_root = os.path.join(self.repo_root, "scss")
    self.sass_dest_root = os.path.join(self.repo_root, "gh-pages/public/stylesheets")
    self.sass_default_options = {
      "output_style" : "nested",
      "include_paths" : [
        os.path.join(self.repo_root, "govuk_frontend_toolkit/stylesheets/"),
        os.path.join(self.repo_root, "scss"),
        os.path.join(self.repo_root, "gh-pages/assets/scss")
      ]
    }
    self.clean()

  def compile_file(self, src_path_abs):
    sass_options = self.sass_default_options
    sass_options["filename"] = src_path_abs
    dest_path_abs = src_path_abs.replace(self.sass_src_root, self.sass_dest_root)
    dest_path_abs = self.__change_extension_to(dest_path_abs, "css")
    result = sass.compile(**sass_options)
    open(dest_path_abs, "w+").write(result)

  def compile(self):
    for root, dirs, files in os.walk(self.sass_src_root):
      for dir in dirs:
        dest_dir = os.path.join(self.sass_dest_root, dir)
        if os.path.isdir(dest_dir) is False:
          os.mkdir(dest_dir)

      for file in files:
        if self.__get_filename_parts(file)['extension'] is '.scss':
          self.compile_file(os.path.join(root, file))

  def clean(self):
    shutil.rmtree(self.sass_dest_root)
    os.mkdir(self.sass_dest_root)

  def __change_extension_to(self, filename, new_extension):
    print filename
    file = self.__get_filename_parts(filename)
    return file['name'] + "." + new_extension

  def __get_filename_parts(self, filename):
    name, extension = os.path.splitext(filename)
    file = {
      'name': name,
      'extension': extension
    }
    return file
