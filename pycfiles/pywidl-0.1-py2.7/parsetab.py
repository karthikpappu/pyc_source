# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywidl/parsetab.py
# Compiled at: 2012-03-24 03:57:04
_tabversion = '3.2'
_lr_method = 'LALR'
_lr_signature = b' \xab\xf8^o\xa4\x06W\xca\xbc\x8c\xc9\x1d\xda\r\xfe'
_lr_action_items = {'partial': ([0, 1, 2, 4, 6, 8, 9, 10, 12, 13, 17, 18, 34, 35, 36, 72, 98, 120, 150, 180, 186, 190, 191, 214], [-2, -85, 5, -8, -3, -5, -7, -11, -1, -6, -4, -9, -10, -12, -13, -84, -40, -39, -34, -15, -20, -14, -29, -38]), 'sequence': ([7, 28, 40, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 43, -85, 43, 43, -84, 43, -17, 43, -85, -17, -85, -85, 43, -85, -85, 43, 43, -85, 43, -85, -63, -85, -81, -82, -85, -16, -18, -66, -60, -65, -19, 43, -61, -64, -67, -68, -48, -49, 43, -63, 43, -52, -50, -53, -51, -59, -62, -83, 43, -23, -85, -41, -54, -69]), 'true': ([198, 229], [217, 217]), 'attribute': ([72, 78, 103, 116, 130, 139, 163, 164, 168, 169, 170, 175, 176, 177, 199, 200, 201, 203, 204, 205, 206, 235, 237, 238], [-84, -17, -17, -85, -85, -56, -16, -18, -19, -56, -58, -48, -55, -49, -52, -50, -53, -51, -57, 226, -59, -41, -54, -69]), 'float': ([7, 28, 40, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 156, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 44, -85, 44, 44, -84, 44, -17, 44, -85, -17, -85, -85, 44, -85, -85, 44, 44, -85, 44, -85, -63, -85, -81, -82, 44, -85, -16, -18, -66, -60, -65, -19, 44, -61, -64, -67, -68, -48, -49, 44, -63, 44, -52, -50, -53, -51, -59, -62, -83, 44, -23, -85, -41, -54, -69]), ',': ([21, 22, 23, 24, 25, 26, 73, 75, 77, 101, 109, 113, 134, 149, 160, 161, 162, 197, 198, 215, 216, 217, 218, 219, 220, 221, 222, 223], [39, -91, -89, -90, -88, -130, 39, 110, -132, 128, -131, -76, 110, 128, -78, -25, -133, -77, -28, -47, -27, -46, -24, -44, -42, -43, -45, -26]), 'boolean': ([7, 28, 40, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 156, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 47, -85, 47, 47, -84, 47, -17, 47, -85, -17, -85, -85, 47, -85, -85, 47, 47, -85, 47, -85, -63, -85, -81, -82, 47, -85, -16, -18, -66, -60, -65, -19, 47, -61, -64, -67, -68, -48, -49, 47, -63, 47, -52, -50, -53, -51, -59, -62, -83, 47, -23, -85, -41, -54, -69]), 'static': ([72, 78, 103, 116, 130, 139, 163, 164, 168, 175, 177, 199, 200, 201, 203, 206, 235, 237, 238], [-84, -17, -17, -85, -85, 166, -16, -18, -19, -48, -49, -52, -50, -53, -51, -59, -41, -54, -69]), 'false': ([198, 229], [215, 215]), 'null': ([198, 229], [222, 222]), 'byte': ([7, 28, 40, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 156, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 60, -85, 60, 60, -84, 60, -17, 60, -85, -17, -85, -85, 60, -85, -85, 60, 60, -85, 60, -85, -63, -85, -81, -82, 60, -85, -16, -18, -66, -60, -65, -19, 60, -61, -64, -67, -68, -48, -49, 60, -63, 60, -52, -50, -53, -51, -59, -62, -83, 60, -23, -85, -41, -54, -69]), 'setter': ([72, 78, 103, 116, 130, 139, 163, 164, 165, 167, 168, 172, 173, 174, 175, 177, 179, 199, 200, 201, 203, 206, 235, 237, 238], [-84, -17, -17, -85, -85, 167, -16, -18, -66, -65, -19, -64, -67, -68, -48, -49, 167, -52, -50, -53, -51, -59, -41, -54, -69]), 'typedef': ([0, 1, 2, 4, 6, 8, 9, 10, 12, 13, 17, 18, 34, 35, 36, 72, 98, 120, 150, 180, 186, 190, 191, 214], [-2, -85, 7, -8, -3, -5, -7, -11, -1, -6, -4, -9, -10, -12, -13, -84, -40, -39, -34, -15, -20, -14, -29, -38]), 'const': ([72, 78, 103, 104, 116, 130, 132, 139, 153, 154, 157, 163, 164, 168, 175, 177, 199, 200, 201, 203, 206, 211, 235, 237, 238], [-84, -17, -17, -85, -85, -85, 156, 156, -81, -82, -85, -16, -18, -19, -48, -49, -52, -50, -53, -51, -59, -83, -41, -54, -69]), 'dictionary': ([0, 1, 2, 4, 6, 8, 9, 10, 12, 13, 17, 18, 34, 35, 36, 72, 98, 120, 150, 180, 186, 190, 191, 214], [-2, -85, 14, -8, -3, -5, -7, -11, -1, -6, -4, -9, -10, -12, -13, -84, -40, -39, -34, -15, -20, -14, -29, -38]), ')': ([40, 44, 45, 47, 52, 53, 54, 55, 57, 58, 59, 60, 62, 63, 64, 74, 75, 80, 82, 83, 88, 90, 91, 92, 93, 94, 95, 96, 111, 113, 115, 118, 119, 121, 123, 133, 134, 138, 141, 142, 143, 144, 145, 158, 159, 160, 161, 181, 182, 183, 185, 197, 198, 208, 209, 215, 216, 217, 218, 219, 220, 221, 222, 223, 227, 230, 233], [-73, -113, -123, -110, -112, -120, -123, -123, -123, -123, -116, -111, -117, -114, -109, 109, -75, -102, -125, -115, -123, -97, -118, -119, -107, -104, -103, -106, -72, -76, -73, -123, -122, -123, -98, -73, -75, 162, -127, -121, -124, -123, -101, 196, -74, -78, -25, -105, -126, -99, 209, -77, -28, -101, -96, -47, -27, -46, -24, -44, -42, -43, -45, -26, -100, -73, 236]), '(': ([7, 26, 28, 40, 44, 45, 47, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 71, 72, 76, 77, 78, 79, 80, 82, 83, 86, 91, 92, 93, 94, 95, 96, 97, 100, 103, 104, 105, 106, 107, 110, 114, 115, 116, 118, 119, 121, 124, 126, 130, 132, 133, 139, 141, 142, 143, 148, 153, 154, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 181, 182, 184, 199, 200, 201, 202, 203, 206, 207, 209, 211, 224, 225, 226, 228, 230, 235, 237, 238], [-85, 40, 51, -85, -113, -123, -110, -92, -125, 51, -112, -120, -123, -123, -94, -123, -123, -116, -111, -123, -117, -114, -109, 51, -84, 51, 115, -17, 51, -102, -125, -115, -95, -118, -119, -107, -104, -103, -106, -93, -85, -17, -85, -128, -129, 133, -85, 51, -85, -85, -123, -122, -123, 51, 51, -85, 51, -85, -63, -127, -121, -124, -85, -81, -82, -85, -16, -18, -66, -60, -65, -19, 51, -61, -64, -67, -68, -48, -49, 51, -63, -105, -126, 51, -52, -50, -53, -71, -51, -59, -62, -96, -83, 230, -70, 51, -23, -85, -41, -54, -69]), 'creator': ([72, 78, 103, 116, 130, 139, 163, 164, 165, 167, 168, 172, 173, 174, 175, 177, 179, 199, 200, 201, 203, 206, 235, 237, 238], [-84, -17, -17, -85, -85, 165, -16, -18, -66, -65, -19, -64, -67, -68, -48, -49, 165, -52, -50, -53, -51, -59, -41, -54, -69]), 'octet': ([7, 28, 40, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 156, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 52, -85, 52, 52, -84, 52, -17, 52, -85, -17, -85, -85, 52, -85, -85, 52, 52, -85, 52, -85, -63, -85, -81, -82, 52, -85, -16, -18, -66, -60, -65, -19, 52, -61, -64, -67, -68, -48, -49, 52, -63, 52, -52, -50, -53, -51, -59, -62, -83, 52, -23, -85, -41, -54, -69]), 'unsigned': ([7, 28, 40, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 156, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 46, -85, 46, 46, -84, 46, -17, 46, -85, -17, -85, -85, 46, -85, -85, 46, 46, -85, 46, -85, -63, -85, -81, -82, 46, -85, -16, -18, -66, -60, -65, -19, 46, -61, -64, -67, -68, -48, -49, 46, -63, 46, -52, -50, -53, -51, -59, -62, -83, 46, -23, -85, -41, -54, -69]), 'long': ([7, 28, 40, 46, 51, 53, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 156, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 53, -85, 53, 53, 92, 53, -84, 53, -17, 53, -85, -17, -85, -85, 53, -85, -85, 53, 53, -85, 53, -85, -63, -85, -81, -82, 53, -85, -16, -18, -66, -60, -65, -19, 53, -61, -64, -67, -68, -48, -49, 53, -63, 53, -52, -50, -53, -51, -59, -62, -83, 53, -23, -85, -41, -54, -69]), 'any': ([7, 28, 40, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 50, -85, 87, 50, -84, 50, -17, 50, -85, -17, -85, -85, 50, -85, -85, 87, 50, -85, 50, -85, -63, -85, -81, -82, -85, -16, -18, -66, -60, -65, -19, 50, -61, -64, -67, -68, -48, -49, 50, -63, 87, -52, -50, -53, -51, -59, -62, -83, 50, -23, -85, -41, -54, -69]), 'readonly': ([72, 78, 103, 116, 130, 139, 163, 164, 168, 169, 170, 175, 176, 177, 199, 200, 201, 203, 206, 235, 237, 238], [-84, -17, -17, -85, -85, -56, -16, -18, -19, -56, 204, -48, -55, -49, -52, -50, -53, -51, -59, -41, -54, -69]), ':': ([30, 32, 33], [66, 66, 66]), 'optional': ([40, 72, 76, 110, 115, 133, 230], [-85, -84, 114, -85, -85, -85, -85]), 'Date': ([7, 28, 40, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 54, -85, 54, 54, -84, 54, -17, 54, -85, -17, -85, -85, 54, -85, -85, 54, 54, -85, 54, -85, -63, -85, -81, -82, -85, -16, -18, -66, -60, -65, -19, 54, -61, -64, -67, -68, -48, -49, 54, -63, 54, -52, -50, -53, -51, -59, -62, -83, 54, -23, -85, -41, -54, -69]), 'ELLIPSIS': ([44, 45, 47, 48, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 80, 82, 83, 86, 91, 92, 93, 94, 95, 96, 97, 112, 118, 119, 121, 141, 142, 143, 181, 182, 209], [-113, -123, -110, -92, -125, -112, -120, -123, -123, -94, -123, -123, -116, -111, -123, -117, -114, -109, -102, -125, -115, -95, -118, -119, -107, -104, -103, -106, -93, 136, -123, -122, -123, -127, -121, -124, -105, -126, -96]), ';': ([65, 84, 129, 140, 146, 151, 152, 169, 187, 192, 196, 198, 210, 215, 216, 217, 218, 219, 220, 221, 222, 223, 232, 234, 236], [98, 120, 150, 180, 186, 190, 191, 201, -25, 211, 214, -28, 228, -47, -27, -46, -24, -44, -42, -43, -45, -26, 235, 237, 238]), 'IDENTIFIER': ([0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 27, 28, 29, 34, 35, 36, 39, 40, 41, 44, 45, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 71, 72, 76, 78, 79, 80, 82, 83, 86, 91, 92, 93, 94, 95, 96, 97, 98, 100, 103, 104, 105, 106, 110, 112, 114, 115, 116, 118, 119, 120, 121, 124, 126, 130, 132, 133, 135, 136, 137, 139, 141, 142, 143, 147, 148, 150, 153, 154, 155, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 180, 181, 182, 184, 186, 190, 191, 193, 194, 199, 200, 201, 202, 203, 206, 207, 209, 211, 213, 214, 226, 228, 230, 231, 235, 237, 238], [-2, -85, 11, 26, -8, -3, -85, -5, -7, -11, -1, -6, 30, 31, 32, -4, -9, 33, 37, 42, 55, 65, -10, -12, -13, 26, -85, 77, -113, -123, -110, -92, 84, -125, 55, -112, -120, -123, -123, -94, -123, -123, -116, -111, -123, -117, -114, -109, 99, 55, -84, 55, -17, 55, -102, -125, -115, -95, -118, -119, -107, -104, -103, -106, -93, -40, -85, -17, -85, -128, -129, -85, -80, 55, -85, -85, -123, -122, -39, -123, 55, 55, -85, 55, -85, 160, -79, 161, -63, -127, -121, -124, 187, -85, -34, -81, -82, 192, -85, -16, -18, -66, -60, -65, -19, 55, -61, -64, -67, -68, -48, -49, 55, -63, -15, -105, -126, 55, -20, -14, -29, 212, -127, -52, -50, -53, 225, -51, -59, -62, -96, -83, -108, -38, 55, -23, -85, 234, -41, -54, -69]), '=': ([26, 37, 161, 187, 212], [41, 71, 198, 198, 229]), '<': ([43], [79]), '?': ([44, 45, 47, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64, 83, 88, 91, 92, 118, 121, 141, 144, 194, 209], [-113, 82, -110, -112, -120, 82, 82, 82, 82, -116, -111, 82, -117, -114, -109, -115, 82, -118, -119, 82, 82, 182, 82, 182, -96]), '$end': ([0, 1, 4, 6, 8, 9, 10, 12, 13, 17, 18, 34, 35, 36, 98, 120, 150, 180, 186, 190, 191, 214], [-2, 0, -8, -3, -5, -7, -11, -1, -6, -4, -9, -10, -12, -13, -40, -39, -34, -15, -20, -14, -29, -38]), 'stringifier': ([72, 78, 103, 116, 130, 139, 163, 164, 168, 175, 177, 199, 200, 201, 203, 206, 235, 237, 238], [-84, -17, -17, -85, -85, 169, -16, -18, -19, -48, -49, -52, -50, -53, -51, -59, -41, -54, -69]), 'object': ([7, 28, 40, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 58, -85, 58, 58, -84, 58, -17, 58, -85, -17, -85, -85, 58, -85, -85, 58, 58, -85, 58, -85, -63, -85, -81, -82, -85, -16, -18, -66, -60, -65, -19, 58, -61, -64, -67, -68, -48, -49, 58, -63, 58, -52, -50, -53, -51, -59, -62, -83, 58, -23, -85, -41, -54, -69]), 'STRING': ([68, 128, 198], [101, 149, 216]), 'DOMString': ([7, 28, 40, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 57, -85, 57, 57, -84, 57, -17, 57, -85, -17, -85, -85, 57, -85, -85, 57, 57, -85, 57, -85, -63, -85, -81, -82, -85, -16, -18, -66, -60, -65, -19, 57, -61, -64, -67, -68, -48, -49, 57, -63, 57, -52, -50, -53, -51, -59, -62, -83, 57, -23, -85, -41, -54, -69]), 'void': ([71, 72, 78, 103, 116, 130, 139, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 199, 200, 201, 203, 206, 207, 235, 237, 238], [106, -84, -17, -17, -85, -85, -63, -16, -18, -66, -60, -65, -19, 106, -61, -64, -67, -68, -48, -49, 106, -63, -52, -50, -53, -51, -59, -62, -41, -54, -69]), 'enum': ([0, 1, 2, 4, 6, 8, 9, 10, 12, 13, 17, 18, 34, 35, 36, 72, 98, 120, 150, 180, 186, 190, 191, 214], [-2, -85, 15, -8, -3, -5, -7, -11, -1, -6, -4, -9, -10, -12, -13, -84, -40, -39, -34, -15, -20, -14, -29, -38]), 'legacycaller': ([72, 78, 103, 116, 130, 139, 163, 164, 165, 167, 168, 172, 173, 174, 175, 177, 179, 199, 200, 201, 203, 206, 235, 237, 238], [-84, -17, -17, -85, -85, 174, -16, -18, -66, -65, -19, -64, -67, -68, -48, -49, 174, -52, -50, -53, -51, -59, -41, -54, -69]), 'getter': ([72, 78, 103, 116, 130, 139, 163, 164, 165, 167, 168, 172, 173, 174, 175, 177, 179, 199, 200, 201, 203, 206, 235, 237, 238], [-84, -17, -17, -85, -85, 172, -16, -18, -66, -65, -19, -64, -67, -68, -48, -49, 172, -52, -50, -53, -51, -59, -41, -54, -69]), 'INTEGER': ([198, 229], [221, 221]), 'interface': ([0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 17, 18, 20, 34, 35, 36, 72, 98, 120, 150, 180, 186, 190, 191, 214], [-2, -85, 16, -8, 27, -3, -5, -7, -11, -1, -6, -4, -9, 16, -10, -12, -13, -84, -40, -39, -34, -15, -20, -14, -29, -38]), '[': ([0, 1, 4, 6, 7, 8, 9, 10, 12, 13, 17, 18, 34, 35, 36, 40, 44, 45, 47, 50, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64, 78, 82, 83, 87, 88, 91, 92, 98, 100, 103, 104, 110, 115, 116, 118, 120, 121, 130, 133, 144, 148, 150, 153, 154, 157, 163, 164, 168, 175, 177, 180, 186, 190, 191, 199, 200, 201, 203, 206, 209, 211, 214, 228, 230, 235, 237, 238], [-2, 3, -8, -3, 3, -5, -7, -11, -1, -6, -4, -9, -10, -12, -13, 3, -113, 81, -110, 85, -112, -120, 81, 81, 81, 81, -116, -111, 81, -117, -114, -109, -17, 85, -115, 122, 81, -118, -119, -40, 3, -17, 3, 3, 3, 3, 81, -39, 81, 3, 3, 81, 3, -34, -81, -82, 3, -16, -18, -19, -48, -49, -15, -20, -14, -29, -52, -50, -53, -51, -59, -96, -83, -38, -23, 3, -41, -54, -69]), ']': ([21, 22, 23, 24, 25, 26, 38, 73, 77, 81, 85, 108, 109, 122, 162], [-87, -91, -89, -90, -88, -130, 72, -87, -132, 118, 121, -86, -131, 144, -133]), 'deleter': ([72, 78, 103, 116, 130, 139, 163, 164, 165, 167, 168, 172, 173, 174, 175, 177, 179, 199, 200, 201, 203, 206, 235, 237, 238], [-84, -17, -17, -85, -85, 173, -16, -18, -66, -65, -19, -64, -67, -68, -48, -49, 173, -52, -50, -53, -51, -59, -41, -54, -69]), 'implements': ([11], [29]), 'exception': ([0, 1, 2, 4, 6, 8, 9, 10, 12, 13, 17, 18, 34, 35, 36, 72, 98, 120, 150, 180, 186, 190, 191, 214], [-2, -85, 19, -8, -3, -5, -7, -11, -1, -6, -4, -9, -10, -12, -13, -84, -40, -39, -34, -15, -20, -14, -29, -38]), 'short': ([7, 28, 40, 46, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 156, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 62, -85, 62, 62, 62, -84, 62, -17, 62, -85, -17, -85, -85, 62, -85, -85, 62, 62, -85, 62, -85, -63, -85, -81, -82, 62, -85, -16, -18, -66, -60, -65, -19, 62, -61, -64, -67, -68, -48, -49, 62, -63, 62, -52, -50, -53, -51, -59, -62, -83, 62, -23, -85, -41, -54, -69]), 'double': ([7, 28, 40, 51, 71, 72, 76, 78, 79, 100, 103, 104, 110, 114, 115, 116, 124, 126, 130, 132, 133, 139, 148, 153, 154, 156, 157, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 174, 175, 177, 178, 179, 184, 199, 200, 201, 203, 206, 207, 211, 226, 228, 230, 235, 237, 238], [-85, 63, -85, 63, 63, -84, 63, -17, 63, -85, -17, -85, -85, 63, -85, -85, 63, 63, -85, 63, -85, -63, -85, -81, -82, 63, -85, -16, -18, -66, -60, -65, -19, 63, -61, -64, -67, -68, -48, -49, 63, -63, 63, -52, -50, -53, -51, -59, -62, -83, 63, -23, -85, -41, -54, -69]), 'FLOAT': ([198, 229], [219, 219]), 'inherit': ([72, 78, 103, 116, 130, 139, 163, 164, 168, 169, 175, 177, 199, 200, 201, 203, 206, 235, 237, 238], [-84, -17, -17, -85, -85, 176, -16, -18, -19, 176, -48, -49, -52, -50, -53, -51, -59, -41, -54, -69]), 'callback': ([0, 1, 2, 4, 6, 8, 9, 10, 12, 13, 17, 18, 34, 35, 36, 72, 98, 120, 150, 180, 186, 190, 191, 214], [-2, -85, 20, -8, -3, -5, -7, -11, -1, -6, -4, -9, -10, -12, -13, -84, -40, -39, -34, -15, -20, -14, -29, -38]), '{': ([30, 31, 32, 33, 42, 67, 69, 70, 99], [-33, 68, -33, -33, 78, 100, 103, 104, -32]), '>': ([44, 45, 47, 48, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 80, 82, 83, 86, 91, 92, 93, 94, 95, 96, 97, 117, 118, 119, 121, 141, 142, 143, 181, 182, 209], [-113, -123, -110, -92, -125, -112, -120, -123, -123, -94, -123, -123, -116, -111, -123, -117, -114, -109, -102, -125, -115, -95, -118, -119, -107, -104, -103, -106, -93, 141, -123, -122, -123, -127, -121, -124, -105, -126, -96]), '}': ([78, 100, 101, 102, 103, 104, 116, 125, 127, 130, 131, 148, 149, 153, 154, 157, 163, 164, 168, 175, 177, 188, 189, 195, 199, 200, 201, 203, 206, 211, 228, 235, 237, 238], [-17, -22, -37, 129, -17, -31, 140, 146, -35, 151, 152, -22, -37, -81, -82, -31, -16, -18, -19, -48, -49, -21, -36, -30, -52, -50, -53, -51, -59, -83, -23, -41, -54, -69]), 'or': ([44, 45, 47, 52, 53, 54, 55, 57, 58, 59, 60, 62, 63, 64, 80, 82, 83, 88, 89, 90, 91, 92, 93, 94, 95, 96, 118, 119, 121, 123, 141, 142, 143, 144, 145, 181, 182, 183, 208, 209], [-113, -123, -110, -112, -120, -123, -123, -123, -123, -116, -111, -117, -114, -109, -102, -125, -115, -123, 124, -97, -118, -119, -107, -104, -103, -106, -123, -122, -123, -98, -127, -121, -124, -123, 184, -105, -126, -99, 184, -96])}
_lr_action = {}
for _k, _v in _lr_action_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_action:
            _lr_action[_x] = {}
        _lr_action[_x][_k] = _y

del _lr_action_items
_lr_goto_items = {'CallbackRestOrInterface': ([20], [34]), 'Const': ([132, 139], [153, 164]), 'Inheritance': ([30, 32, 33], [67, 69, 70]), 'CallbackOrInterface': ([2], [6]), 'OptionalIdentifier': ([202], [224]), 'Typedef': ([2], [4]), 'PrimitiveType': ([28, 51, 71, 76, 79, 114, 124, 126, 132, 156, 169, 178, 184, 226], [45, 45, 45, 45, 45, 45, 45, 45, 45, 194, 45, 45, 45, 45]), 'Argument': ([40, 110, 115, 133, 230], [75, 134, 75, 75, 75]), 'ReturnType': ([71, 169, 178], [107, 202, 202]), 'CallbackRest': ([20], [35]), 'Arguments': ([75, 134], [111, 159]), 'SingleType': ([28, 71, 76, 79, 114, 126, 132, 169, 178, 226], [48, 48, 48, 48, 48, 48, 48, 48, 48, 48]), 'ExceptionField': ([132], [154]), 'Ellipsis': ([112], [135]), 'Type': ([28, 71, 76, 79, 114, 126, 132, 169, 178, 226], [49, 105, 112, 117, 137, 147, 155, 105, 105, 231]), 'UnionMemberTypes': ([145, 208], [185, 227]), 'ArgumentList': ([40, 115, 133, 230], [74, 138, 158, 233]), 'DictionaryMembers': ([100, 148], [125, 188]), 'Dictionary': ([2], [8]), 'StringifierAttributeOrOperation': ([169], [200]), 'UnionType': ([28, 51, 71, 76, 79, 114, 124, 126, 132, 169, 178, 184, 226], [61, 88, 61, 61, 61, 61, 88, 61, 61, 61, 61, 88, 61]), 'ConstValue': ([198, 229], [223, 232]), 'Enum': ([2], [9]), 'TypeSuffixStartingWithArray': ([50, 82], [86, 119]), 'UnionMemberType': ([51, 124, 184], [89, 145, 208]), 'ExtendedAttribute': ([3, 39], [21, 73]), 'OptionalOrRequiredArgument': ([76], [113]), 'ExtendedAttributeList': ([1, 7, 40, 100, 104, 110, 115, 116, 130, 133, 148, 157, 230], [2, 28, 76, 126, 132, 76, 76, 139, 139, 76, 126, 132, 76]), 'Interface': ([2, 20], [10, 36]), 'ReadOnly': ([170], [205]), 'DefaultValue': ([198], [218]), 'InterfaceMembers': ([78, 103], [116, 130]), 'Definition': ([2], [12]), 'Exception': ([2], [13]), 'NonAnyType': ([28, 51, 71, 76, 79, 114, 124, 126, 132, 169, 178, 184, 226], [56, 90, 56, 56, 56, 56, 90, 56, 56, 56, 56, 90, 56]), 'Default': ([161, 187], [197, 210]), 'ExceptionMember': ([132], [157]), 'EnumValues': ([101, 149], [127, 189]), 'Inherit': ([139, 169], [170, 170]), 'ExtendedAttributeArgList': ([3, 39], [23, 23]), 'Specials': ([139, 179], [171, 207]), 'DictionaryMember': ([126], [148]), 'IntegerType': ([28, 46, 51, 71, 76, 79, 114, 124, 126, 132, 156, 169, 178, 184, 226], [59, 83, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59]), 'ExtendedAttributeIdent': ([3, 39], [24, 24]), 'ExtendedAttributeNoArgs': ([3, 39], [25, 25]), 'Definitions': ([0], [1]), 'BooleanLiteral': ([198, 229], [220, 220]), 'PartialInterface': ([2], [17]), 'ImplementsStatement': ([2], [18]), 'ConstType': ([156], [193]), 'InterfaceMember': ([139], [163]), 'EnumValueList': ([68], [102]), 'Attribute': ([139, 169], [175, 203]), 'ExtendedAttributes': ([21, 73], [38, 108]), 'ExceptionMembers': ([104, 157], [131, 195]), 'ExtendedAttributeNamedArgList': ([3, 39], [22, 22]), 'UnsignedIntegerType': ([28, 51, 71, 76, 79, 114, 124, 126, 132, 156, 169, 178, 184, 226], [64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64]), 'TypeSuffix': ([45, 54, 55, 57, 58, 61, 88, 118, 121, 144], [80, 93, 94, 95, 96, 97, 123, 142, 143, 183]), 'OptionalLong': ([53], [91]), 'AttributeOrOperation': ([139], [168]), 'OperationRest': ([169, 178], [199, 206]), 'Operation': ([139], [177]), 'Null': ([141, 194], [181, 213]), 'Qualifiers': ([139], [178]), 'Special': ([139, 179], [179, 179])}
_lr_goto = {}
for _k, _v in _lr_goto_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_goto:
            _lr_goto[_x] = {}
        _lr_goto[_x][_k] = _y

del _lr_goto_items
_lr_productions = [
 (
  "S' -> Definitions", "S'", 1, None, None, None),
 (
  'Definitions -> Definitions ExtendedAttributeList Definition', 'Definitions', 3, 'p_Definitions', '/home/vasily/dev/pywidl/pywidl/grammar.py', 15),
 (
  'Definitions -> <empty>', 'Definitions', 0, 'p_Definitions_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 23),
 (
  'Definition -> CallbackOrInterface', 'Definition', 1, 'p_Definition', '/home/vasily/dev/pywidl/pywidl/grammar.py', 30),
 (
  'Definition -> PartialInterface', 'Definition', 1, 'p_Definition', '/home/vasily/dev/pywidl/pywidl/grammar.py', 31),
 (
  'Definition -> Dictionary', 'Definition', 1, 'p_Definition', '/home/vasily/dev/pywidl/pywidl/grammar.py', 32),
 (
  'Definition -> Exception', 'Definition', 1, 'p_Definition', '/home/vasily/dev/pywidl/pywidl/grammar.py', 33),
 (
  'Definition -> Enum', 'Definition', 1, 'p_Definition', '/home/vasily/dev/pywidl/pywidl/grammar.py', 34),
 (
  'Definition -> Typedef', 'Definition', 1, 'p_Definition', '/home/vasily/dev/pywidl/pywidl/grammar.py', 35),
 (
  'Definition -> ImplementsStatement', 'Definition', 1, 'p_Definition', '/home/vasily/dev/pywidl/pywidl/grammar.py', 36),
 (
  'CallbackOrInterface -> callback CallbackRestOrInterface', 'CallbackOrInterface', 2, 'p_CallbackOrInterface_callback', '/home/vasily/dev/pywidl/pywidl/grammar.py', 44),
 (
  'CallbackOrInterface -> Interface', 'CallbackOrInterface', 1, 'p_CallbackOrInterface_interface', '/home/vasily/dev/pywidl/pywidl/grammar.py', 51),
 (
  'CallbackRestOrInterface -> CallbackRest', 'CallbackRestOrInterface', 1, 'p_CallbackRestOrInterface', '/home/vasily/dev/pywidl/pywidl/grammar.py', 58),
 (
  'CallbackRestOrInterface -> Interface', 'CallbackRestOrInterface', 1, 'p_CallbackRestOrInterface_interface', '/home/vasily/dev/pywidl/pywidl/grammar.py', 65),
 (
  'Interface -> interface IDENTIFIER Inheritance { InterfaceMembers } ;', 'Interface', 7, 'p_Interface', '/home/vasily/dev/pywidl/pywidl/grammar.py', 73),
 (
  'PartialInterface -> partial interface IDENTIFIER { InterfaceMembers } ;', 'PartialInterface', 7, 'p_PartialInterface', '/home/vasily/dev/pywidl/pywidl/grammar.py', 81),
 (
  'InterfaceMembers -> InterfaceMembers ExtendedAttributeList InterfaceMember', 'InterfaceMembers', 3, 'p_InterfaceMembers', '/home/vasily/dev/pywidl/pywidl/grammar.py', 89),
 (
  'InterfaceMembers -> <empty>', 'InterfaceMembers', 0, 'p_InterfaceMembers_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 97),
 (
  'InterfaceMember -> Const', 'InterfaceMember', 1, 'p_InterfaceMember', '/home/vasily/dev/pywidl/pywidl/grammar.py', 104),
 (
  'InterfaceMember -> AttributeOrOperation', 'InterfaceMember', 1, 'p_InterfaceMember', '/home/vasily/dev/pywidl/pywidl/grammar.py', 105),
 (
  'Dictionary -> dictionary IDENTIFIER Inheritance { DictionaryMembers } ;', 'Dictionary', 7, 'p_Dictionary', '/home/vasily/dev/pywidl/pywidl/grammar.py', 113),
 (
  'DictionaryMembers -> ExtendedAttributeList DictionaryMember DictionaryMembers', 'DictionaryMembers', 3, 'p_DictionaryMembers', '/home/vasily/dev/pywidl/pywidl/grammar.py', 121),
 (
  'DictionaryMembers -> <empty>', 'DictionaryMembers', 0, 'p_DictionaryMembers_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 129),
 (
  'DictionaryMember -> Type IDENTIFIER Default ;', 'DictionaryMember', 4, 'p_DictionaryMember', '/home/vasily/dev/pywidl/pywidl/grammar.py', 136),
 (
  'Default -> = DefaultValue', 'Default', 2, 'p_Default', '/home/vasily/dev/pywidl/pywidl/grammar.py', 144),
 (
  'Default -> <empty>', 'Default', 0, 'p_Default_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 151),
 (
  'DefaultValue -> ConstValue', 'DefaultValue', 1, 'p_DefaultValue', '/home/vasily/dev/pywidl/pywidl/grammar.py', 159),
 (
  'DefaultValue -> STRING', 'DefaultValue', 1, 'p_DefaultValue_string', '/home/vasily/dev/pywidl/pywidl/grammar.py', 166),
 (
  'DefaultValue -> <empty>', 'DefaultValue', 0, 'p_DefaultValue_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 173),
 (
  'Exception -> exception IDENTIFIER Inheritance { ExceptionMembers } ;', 'Exception', 7, 'p_Exception', '/home/vasily/dev/pywidl/pywidl/grammar.py', 180),
 (
  'ExceptionMembers -> ExtendedAttributeList ExceptionMember ExceptionMembers', 'ExceptionMembers', 3, 'p_ExceptionMembers', '/home/vasily/dev/pywidl/pywidl/grammar.py', 188),
 (
  'ExceptionMembers -> <empty>', 'ExceptionMembers', 0, 'p_ExceptionMembers_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 196),
 (
  'Inheritance -> : IDENTIFIER', 'Inheritance', 2, 'p_Inheritance', '/home/vasily/dev/pywidl/pywidl/grammar.py', 203),
 (
  'Inheritance -> <empty>', 'Inheritance', 0, 'p_Inheritance_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 210),
 (
  'Enum -> enum IDENTIFIER { EnumValueList } ;', 'Enum', 6, 'p_Enum', '/home/vasily/dev/pywidl/pywidl/grammar.py', 217),
 (
  'EnumValueList -> STRING EnumValues', 'EnumValueList', 2, 'p_EnumValueList', '/home/vasily/dev/pywidl/pywidl/grammar.py', 225),
 (
  'EnumValues -> , STRING EnumValues', 'EnumValues', 3, 'p_EnumValues', '/home/vasily/dev/pywidl/pywidl/grammar.py', 232),
 (
  'EnumValues -> <empty>', 'EnumValues', 0, 'p_EnumValues_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 239),
 (
  'CallbackRest -> IDENTIFIER = ReturnType ( ArgumentList ) ;', 'CallbackRest', 7, 'p_CallbackRest', '/home/vasily/dev/pywidl/pywidl/grammar.py', 246),
 (
  'Typedef -> typedef ExtendedAttributeList Type IDENTIFIER ;', 'Typedef', 5, 'p_Typedef', '/home/vasily/dev/pywidl/pywidl/grammar.py', 254),
 (
  'ImplementsStatement -> IDENTIFIER implements IDENTIFIER ;', 'ImplementsStatement', 4, 'p_ImplementsStatement', '/home/vasily/dev/pywidl/pywidl/grammar.py', 262),
 (
  'Const -> const ConstType IDENTIFIER = ConstValue ;', 'Const', 6, 'p_Const', '/home/vasily/dev/pywidl/pywidl/grammar.py', 270),
 (
  'ConstValue -> BooleanLiteral', 'ConstValue', 1, 'p_ConstValue_boolean', '/home/vasily/dev/pywidl/pywidl/grammar.py', 278),
 (
  'ConstValue -> INTEGER', 'ConstValue', 1, 'p_ConstValue_integer', '/home/vasily/dev/pywidl/pywidl/grammar.py', 285),
 (
  'ConstValue -> FLOAT', 'ConstValue', 1, 'p_ConstValue_float', '/home/vasily/dev/pywidl/pywidl/grammar.py', 292),
 (
  'ConstValue -> null', 'ConstValue', 1, 'p_ConstValue_null', '/home/vasily/dev/pywidl/pywidl/grammar.py', 299),
 (
  'BooleanLiteral -> true', 'BooleanLiteral', 1, 'p_BooleanLiteral_true', '/home/vasily/dev/pywidl/pywidl/grammar.py', 305),
 (
  'BooleanLiteral -> false', 'BooleanLiteral', 1, 'p_BooleanLiteral_false', '/home/vasily/dev/pywidl/pywidl/grammar.py', 312),
 (
  'AttributeOrOperation -> Attribute', 'AttributeOrOperation', 1, 'p_AttributeOrOperation', '/home/vasily/dev/pywidl/pywidl/grammar.py', 319),
 (
  'AttributeOrOperation -> Operation', 'AttributeOrOperation', 1, 'p_AttributeOrOperation', '/home/vasily/dev/pywidl/pywidl/grammar.py', 320),
 (
  'AttributeOrOperation -> stringifier StringifierAttributeOrOperation', 'AttributeOrOperation', 2, 'p_AttributeOrOperation_stringifier', '/home/vasily/dev/pywidl/pywidl/grammar.py', 328),
 (
  'StringifierAttributeOrOperation -> Attribute', 'StringifierAttributeOrOperation', 1, 'p_StringifierAttributeOrOperation', '/home/vasily/dev/pywidl/pywidl/grammar.py', 337),
 (
  'StringifierAttributeOrOperation -> OperationRest', 'StringifierAttributeOrOperation', 1, 'p_StringifierAttributeOrOperation', '/home/vasily/dev/pywidl/pywidl/grammar.py', 338),
 (
  'StringifierAttributeOrOperation -> ;', 'StringifierAttributeOrOperation', 1, 'p_StringifierAttributeOrOperation', '/home/vasily/dev/pywidl/pywidl/grammar.py', 339),
 (
  'Attribute -> Inherit ReadOnly attribute Type IDENTIFIER ;', 'Attribute', 6, 'p_Attribute', '/home/vasily/dev/pywidl/pywidl/grammar.py', 347),
 (
  'Inherit -> inherit', 'Inherit', 1, 'p_Inherit_true', '/home/vasily/dev/pywidl/pywidl/grammar.py', 355),
 (
  'Inherit -> <empty>', 'Inherit', 0, 'p_Inherit_false', '/home/vasily/dev/pywidl/pywidl/grammar.py', 362),
 (
  'ReadOnly -> readonly', 'ReadOnly', 1, 'p_ReadOnly_true', '/home/vasily/dev/pywidl/pywidl/grammar.py', 369),
 (
  'ReadOnly -> <empty>', 'ReadOnly', 0, 'p_ReadOnly_false', '/home/vasily/dev/pywidl/pywidl/grammar.py', 376),
 (
  'Operation -> Qualifiers OperationRest', 'Operation', 2, 'p_Operation', '/home/vasily/dev/pywidl/pywidl/grammar.py', 383),
 (
  'Qualifiers -> static', 'Qualifiers', 1, 'p_Qualifiers_static', '/home/vasily/dev/pywidl/pywidl/grammar.py', 390),
 (
  'Qualifiers -> Specials', 'Qualifiers', 1, 'p_Qualifiers_specials', '/home/vasily/dev/pywidl/pywidl/grammar.py', 397),
 (
  'Specials -> Special Specials', 'Specials', 2, 'p_Specials', '/home/vasily/dev/pywidl/pywidl/grammar.py', 404),
 (
  'Specials -> <empty>', 'Specials', 0, 'p_Specials_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 411),
 (
  'Special -> getter', 'Special', 1, 'p_Special_getter', '/home/vasily/dev/pywidl/pywidl/grammar.py', 418),
 (
  'Special -> setter', 'Special', 1, 'p_Special_setter', '/home/vasily/dev/pywidl/pywidl/grammar.py', 425),
 (
  'Special -> creator', 'Special', 1, 'p_Special_creator', '/home/vasily/dev/pywidl/pywidl/grammar.py', 432),
 (
  'Special -> deleter', 'Special', 1, 'p_Special_deleter', '/home/vasily/dev/pywidl/pywidl/grammar.py', 439),
 (
  'Special -> legacycaller', 'Special', 1, 'p_Special_legacycaller', '/home/vasily/dev/pywidl/pywidl/grammar.py', 446),
 (
  'OperationRest -> ReturnType OptionalIdentifier ( ArgumentList ) ;', 'OperationRest', 6, 'p_OperationRest', '/home/vasily/dev/pywidl/pywidl/grammar.py', 453),
 (
  'OptionalIdentifier -> IDENTIFIER', 'OptionalIdentifier', 1, 'p_OptionalIdentifier', '/home/vasily/dev/pywidl/pywidl/grammar.py', 461),
 (
  'OptionalIdentifier -> <empty>', 'OptionalIdentifier', 0, 'p_OptionalIdentifier_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 468),
 (
  'ArgumentList -> Argument Arguments', 'ArgumentList', 2, 'p_ArgumentList', '/home/vasily/dev/pywidl/pywidl/grammar.py', 475),
 (
  'ArgumentList -> <empty>', 'ArgumentList', 0, 'p_ArgumentList_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 482),
 (
  'Arguments -> , Argument Arguments', 'Arguments', 3, 'p_Arguments', '/home/vasily/dev/pywidl/pywidl/grammar.py', 489),
 (
  'Arguments -> <empty>', 'Arguments', 0, 'p_Arguments_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 496),
 (
  'Argument -> ExtendedAttributeList OptionalOrRequiredArgument', 'Argument', 2, 'p_Argument', '/home/vasily/dev/pywidl/pywidl/grammar.py', 503),
 (
  'OptionalOrRequiredArgument -> optional Type IDENTIFIER Default', 'OptionalOrRequiredArgument', 4, 'p_OptionalOrRequiredArgument_optional', '/home/vasily/dev/pywidl/pywidl/grammar.py', 511),
 (
  'OptionalOrRequiredArgument -> Type Ellipsis IDENTIFIER', 'OptionalOrRequiredArgument', 3, 'p_OptionalOrRequiredArgument', '/home/vasily/dev/pywidl/pywidl/grammar.py', 518),
 (
  'Ellipsis -> ELLIPSIS', 'Ellipsis', 1, 'p_Ellipsis_true', '/home/vasily/dev/pywidl/pywidl/grammar.py', 533),
 (
  'Ellipsis -> <empty>', 'Ellipsis', 0, 'p_Ellipsis_false', '/home/vasily/dev/pywidl/pywidl/grammar.py', 540),
 (
  'ExceptionMember -> Const', 'ExceptionMember', 1, 'p_ExceptionMember', '/home/vasily/dev/pywidl/pywidl/grammar.py', 547),
 (
  'ExceptionMember -> ExceptionField', 'ExceptionMember', 1, 'p_ExceptionMember', '/home/vasily/dev/pywidl/pywidl/grammar.py', 548),
 (
  'ExceptionField -> Type IDENTIFIER ;', 'ExceptionField', 3, 'p_ExceptionField', '/home/vasily/dev/pywidl/pywidl/grammar.py', 556),
 (
  'ExtendedAttributeList -> [ ExtendedAttribute ExtendedAttributes ]', 'ExtendedAttributeList', 4, 'p_ExtendedAttributeList', '/home/vasily/dev/pywidl/pywidl/grammar.py', 564),
 (
  'ExtendedAttributeList -> <empty>', 'ExtendedAttributeList', 0, 'p_ExtendedAttributeList_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 572),
 (
  'ExtendedAttributes -> , ExtendedAttribute ExtendedAttributes', 'ExtendedAttributes', 3, 'p_ExtendedAttributes', '/home/vasily/dev/pywidl/pywidl/grammar.py', 579),
 (
  'ExtendedAttributes -> <empty>', 'ExtendedAttributes', 0, 'p_ExtendedAttributes_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 586),
 (
  'ExtendedAttribute -> ExtendedAttributeNoArgs', 'ExtendedAttribute', 1, 'p_ExtendedAttribute', '/home/vasily/dev/pywidl/pywidl/grammar.py', 603),
 (
  'ExtendedAttribute -> ExtendedAttributeArgList', 'ExtendedAttribute', 1, 'p_ExtendedAttribute', '/home/vasily/dev/pywidl/pywidl/grammar.py', 604),
 (
  'ExtendedAttribute -> ExtendedAttributeIdent', 'ExtendedAttribute', 1, 'p_ExtendedAttribute', '/home/vasily/dev/pywidl/pywidl/grammar.py', 605),
 (
  'ExtendedAttribute -> ExtendedAttributeNamedArgList', 'ExtendedAttribute', 1, 'p_ExtendedAttribute', '/home/vasily/dev/pywidl/pywidl/grammar.py', 606),
 (
  'Type -> SingleType', 'Type', 1, 'p_Type_single', '/home/vasily/dev/pywidl/pywidl/grammar.py', 693),
 (
  'Type -> UnionType TypeSuffix', 'Type', 2, 'p_Type_union', '/home/vasily/dev/pywidl/pywidl/grammar.py', 700),
 (
  'SingleType -> NonAnyType', 'SingleType', 1, 'p_SingleType', '/home/vasily/dev/pywidl/pywidl/grammar.py', 707),
 (
  'SingleType -> any TypeSuffixStartingWithArray', 'SingleType', 2, 'p_SingleType_any', '/home/vasily/dev/pywidl/pywidl/grammar.py', 714),
 (
  'UnionType -> ( UnionMemberType or UnionMemberType UnionMemberTypes )', 'UnionType', 6, 'p_UnionType', '/home/vasily/dev/pywidl/pywidl/grammar.py', 721),
 (
  'UnionMemberType -> NonAnyType', 'UnionMemberType', 1, 'p_UnionMemberType_nonAnyType', '/home/vasily/dev/pywidl/pywidl/grammar.py', 730),
 (
  'UnionMemberType -> UnionType TypeSuffix', 'UnionMemberType', 2, 'p_UnionMemberType_unionType', '/home/vasily/dev/pywidl/pywidl/grammar.py', 737),
 (
  'UnionMemberType -> any [ ] TypeSuffix', 'UnionMemberType', 4, 'p_UnionMemberType_anyType', '/home/vasily/dev/pywidl/pywidl/grammar.py', 744),
 (
  'UnionMemberTypes -> or UnionMemberType UnionMemberTypes', 'UnionMemberTypes', 3, 'p_UnionMemberTypes', '/home/vasily/dev/pywidl/pywidl/grammar.py', 751),
 (
  'UnionMemberTypes -> <empty>', 'UnionMemberTypes', 0, 'p_UnionMemberTypes_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 758),
 (
  'NonAnyType -> PrimitiveType TypeSuffix', 'NonAnyType', 2, 'p_NonAnyType_primitiveType', '/home/vasily/dev/pywidl/pywidl/grammar.py', 765),
 (
  'NonAnyType -> DOMString TypeSuffix', 'NonAnyType', 2, 'p_NonAnyType_domString', '/home/vasily/dev/pywidl/pywidl/grammar.py', 772),
 (
  'NonAnyType -> IDENTIFIER TypeSuffix', 'NonAnyType', 2, 'p_NonAnyType_interface', '/home/vasily/dev/pywidl/pywidl/grammar.py', 779),
 (
  'NonAnyType -> sequence < Type > Null', 'NonAnyType', 5, 'p_NonAnyType_sequence', '/home/vasily/dev/pywidl/pywidl/grammar.py', 786),
 (
  'NonAnyType -> object TypeSuffix', 'NonAnyType', 2, 'p_NonAnyType_object', '/home/vasily/dev/pywidl/pywidl/grammar.py', 793),
 (
  'NonAnyType -> Date TypeSuffix', 'NonAnyType', 2, 'p_NonAnyType', '/home/vasily/dev/pywidl/pywidl/grammar.py', 800),
 (
  'ConstType -> PrimitiveType Null', 'ConstType', 2, 'p_ConstType', '/home/vasily/dev/pywidl/pywidl/grammar.py', 807),
 (
  'PrimitiveType -> UnsignedIntegerType', 'PrimitiveType', 1, 'p_PrimitiveType_integer', '/home/vasily/dev/pywidl/pywidl/grammar.py', 815),
 (
  'PrimitiveType -> boolean', 'PrimitiveType', 1, 'p_PrimitiveType_boolean', '/home/vasily/dev/pywidl/pywidl/grammar.py', 822),
 (
  'PrimitiveType -> byte', 'PrimitiveType', 1, 'p_PrimitiveType_byte', '/home/vasily/dev/pywidl/pywidl/grammar.py', 829),
 (
  'PrimitiveType -> octet', 'PrimitiveType', 1, 'p_PrimitiveType_octet', '/home/vasily/dev/pywidl/pywidl/grammar.py', 836),
 (
  'PrimitiveType -> float', 'PrimitiveType', 1, 'p_PrimitiveType_float', '/home/vasily/dev/pywidl/pywidl/grammar.py', 843),
 (
  'PrimitiveType -> double', 'PrimitiveType', 1, 'p_PrimitiveType_double', '/home/vasily/dev/pywidl/pywidl/grammar.py', 850),
 (
  'UnsignedIntegerType -> unsigned IntegerType', 'UnsignedIntegerType', 2, 'p_UnsignedIntegerType_unsigned', '/home/vasily/dev/pywidl/pywidl/grammar.py', 857),
 (
  'UnsignedIntegerType -> IntegerType', 'UnsignedIntegerType', 1, 'p_UnsignedIntegerType', '/home/vasily/dev/pywidl/pywidl/grammar.py', 864),
 (
  'IntegerType -> short', 'IntegerType', 1, 'p_IntegerType_short', '/home/vasily/dev/pywidl/pywidl/grammar.py', 871),
 (
  'IntegerType -> long OptionalLong', 'IntegerType', 2, 'p_IntegerType_long', '/home/vasily/dev/pywidl/pywidl/grammar.py', 878),
 (
  'OptionalLong -> long', 'OptionalLong', 1, 'p_OptionalLong_true', '/home/vasily/dev/pywidl/pywidl/grammar.py', 888),
 (
  'OptionalLong -> <empty>', 'OptionalLong', 0, 'p_OptionalLong_false', '/home/vasily/dev/pywidl/pywidl/grammar.py', 895),
 (
  'TypeSuffix -> [ ] TypeSuffix', 'TypeSuffix', 3, 'p_TypeSuffix', '/home/vasily/dev/pywidl/pywidl/grammar.py', 902),
 (
  'TypeSuffix -> ? TypeSuffixStartingWithArray', 'TypeSuffix', 2, 'p_TypeSuffix_null', '/home/vasily/dev/pywidl/pywidl/grammar.py', 909),
 (
  'TypeSuffix -> <empty>', 'TypeSuffix', 0, 'p_TypeSuffix_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 916),
 (
  'TypeSuffixStartingWithArray -> [ ] TypeSuffix', 'TypeSuffixStartingWithArray', 3, 'p_TypeSuffixStartingWithArray', '/home/vasily/dev/pywidl/pywidl/grammar.py', 923),
 (
  'TypeSuffixStartingWithArray -> <empty>', 'TypeSuffixStartingWithArray', 0, 'p_TypeSuffixStartingWithArray_empty', '/home/vasily/dev/pywidl/pywidl/grammar.py', 930),
 (
  'Null -> ?', 'Null', 1, 'p_Null_true', '/home/vasily/dev/pywidl/pywidl/grammar.py', 937),
 (
  'Null -> <empty>', 'Null', 0, 'p_Null_false', '/home/vasily/dev/pywidl/pywidl/grammar.py', 945),
 (
  'ReturnType -> Type', 'ReturnType', 1, 'p_ReturnType', '/home/vasily/dev/pywidl/pywidl/grammar.py', 952),
 (
  'ReturnType -> void', 'ReturnType', 1, 'p_ReturnType_void', '/home/vasily/dev/pywidl/pywidl/grammar.py', 959),
 (
  'ExtendedAttributeNoArgs -> IDENTIFIER', 'ExtendedAttributeNoArgs', 1, 'p_ExtendedAttributeNoArgs', '/home/vasily/dev/pywidl/pywidl/grammar.py', 966),
 (
  'ExtendedAttributeArgList -> IDENTIFIER ( ArgumentList )', 'ExtendedAttributeArgList', 4, 'p_ExtendedAttributeArgList', '/home/vasily/dev/pywidl/pywidl/grammar.py', 974),
 (
  'ExtendedAttributeIdent -> IDENTIFIER = IDENTIFIER', 'ExtendedAttributeIdent', 3, 'p_ExtendedAttributeIdent', '/home/vasily/dev/pywidl/pywidl/grammar.py', 983),
 (
  'ExtendedAttributeNamedArgList -> IDENTIFIER = IDENTIFIER ( ArgumentList )', 'ExtendedAttributeNamedArgList', 6, 'p_ExtendedAttributeNamedArgList', '/home/vasily/dev/pywidl/pywidl/grammar.py', 992)]