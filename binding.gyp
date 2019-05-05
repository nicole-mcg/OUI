{
    'targets': [
      {
        'target_name': 'OUI_Runtime',
        'type': 'executable',
        'sources': [
          'source/main.cpp',
        ],
        'dependencies': ['./lib/OUI-engine/binding.gyp:OUI'],
        'include_dirs': [
          'lib/OUI-engine/include',
        ],
        'copies': [
            {
                'destination': '<(PRODUCT_DIR)/data',
                'files': [
                    'data/fonts/',
                ],
            },
            {
                'destination': '<(PRODUCT_DIR)/data',
                'files': [
                    'data/img/',
                ],
            },
            {
                'destination': '<(PRODUCT_DIR)/data',
                'files': [
                    'data/src/',
                ],
            },
        ],
      },
    ],
  }