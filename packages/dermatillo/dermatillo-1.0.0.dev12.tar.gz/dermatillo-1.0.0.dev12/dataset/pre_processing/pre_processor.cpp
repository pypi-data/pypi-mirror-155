#include <map>
#include <cmath>
#include <vector>
#include <iostream>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

const std::map<int, int> face_mesh_map = {
        {0, 0}, {1, 1}, {2, 2}, {3, 248}, {4, 4}, {5, 5}, {6, 6}, {7, 249}, {8, 8}, {9, 9}, {10, 10}, {11, 11},
        {12, 12}, {13, 13}, {14, 14}, {15, 15}, {16, 16}, {17, 17}, {18, 18}, {19, 19}, {20, 250}, {21, 251},
        {22, 252}, {23, 253}, {24, 254}, {25, 255}, {26, 256}, {27, 257}, {28, 258}, {29, 259}, {30, 260},
        {31, 261}, {32, 262}, {33, 263}, {34, 264}, {35, 265}, {36, 266}, {37, 267}, {38, 268}, {39, 269},
        {40, 270}, {41, 271}, {42, 272}, {43, 273}, {44, 274}, {45, 275}, {46, 276}, {47, 277}, {48, 278},
        {49, 279}, {50, 280}, {51, 281}, {52, 282}, {53, 283}, {54, 284}, {55, 285}, {56, 286}, {57, 287},
        {58, 288}, {59, 289}, {60, 290}, {61, 291}, {62, 292}, {63, 293}, {64, 294}, {65, 295}, {66, 296},
        {67, 297}, {68, 298}, {69, 299}, {70, 300}, {71, 301}, {72, 302}, {73, 303}, {74, 304}, {75, 305},
        {76, 306}, {77, 307}, {78, 308}, {79, 309}, {80, 310}, {81, 311}, {82, 312}, {83, 313}, {84, 314},
        {85, 315}, {86, 316}, {87, 317}, {88, 318}, {89, 319}, {90, 320}, {91, 321}, {92, 322}, {93, 323},
        {94, 94}, {95, 324}, {96, 325}, {97, 326}, {98, 327}, {99, 328}, {100, 329}, {101, 330}, {102, 331},
        {103, 332}, {104, 333}, {105, 334}, {106, 335}, {107, 336}, {108, 337}, {109, 338}, {110, 339}, {111, 340},
        {112, 341}, {113, 342}, {114, 343}, {115, 344}, {116, 345}, {117, 346}, {118, 347}, {119, 348}, {120, 349},
        {121, 350}, {122, 351}, {123, 352}, {124, 353}, {125, 354}, {126, 355}, {127, 356}, {128, 357}, {129, 358},
        {130, 359}, {131, 360}, {132, 361}, {133, 362}, {134, 363}, {135, 364}, {136, 365}, {137, 366}, {138, 367},
        {139, 368}, {140, 369}, {141, 370}, {142, 371}, {143, 372}, {144, 373}, {145, 374}, {146, 375}, {147, 376},
        {148, 377}, {149, 378}, {150, 379}, {151, 151}, {152, 152}, {153, 380}, {154, 381}, {155, 382}, {156, 383},
        {157, 384}, {158, 385}, {159, 386}, {160, 387}, {161, 388}, {162, 389}, {163, 390}, {164, 164}, {165, 391},
        {166, 392}, {167, 393}, {168, 168}, {169, 394}, {170, 395}, {171, 396}, {172, 397}, {173, 398}, {174, 399},
        {175, 175}, {176, 400}, {177, 401}, {178, 402}, {179, 403}, {180, 404}, {181, 405}, {182, 406}, {183, 407},
        {184, 408}, {185, 409}, {186, 410}, {187, 411}, {188, 412}, {189, 413}, {190, 414}, {191, 415}, {192, 416},
        {193, 417}, {194, 418}, {195, 195}, {196, 419}, {197, 197}, {198, 420}, {199, 199}, {200, 200}, {201, 421},
        {202, 422}, {203, 423}, {204, 424}, {205, 425}, {206, 426}, {207, 427}, {208, 428}, {209, 429}, {210, 430},
        {211, 431}, {212, 432}, {213, 433}, {214, 434}, {215, 435}, {216, 436}, {217, 437}, {218, 438}, {219, 439},
        {220, 440}, {221, 441}, {222, 442}, {223, 443}, {224, 444}, {225, 445}, {226, 446}, {227, 447}, {228, 448},
        {229, 449}, {230, 450}, {231, 451}, {232, 452}, {233, 453}, {234, 454}, {235, 455}, {236, 456}, {237, 457},
        {238, 458}, {239, 459}, {240, 460}, {241, 461}, {242, 462}, {243, 463}, {244, 464}, {245, 465}, {246, 466},
        {247, 467}, {248, 3}, {249, 7}, {250, 20}, {251, 21}, {252, 22}, {253, 23}, {254, 24}, {255, 25}, {256, 26},
        {257, 27}, {258, 28}, {259, 29}, {260, 30}, {261, 31}, {262, 32}, {263, 33}, {264, 34}, {265, 35},
        {266, 36}, {267, 37}, {268, 38}, {269, 39}, {270, 40}, {271, 41}, {272, 42}, {273, 43}, {274, 44},
        {275, 45}, {276, 46}, {277, 47}, {278, 48}, {279, 49}, {280, 50}, {281, 51}, {282, 52}, {283, 53},
        {284, 54}, {285, 55}, {286, 56}, {287, 57}, {288, 58}, {289, 59}, {290, 60}, {291, 61}, {292, 62},
        {293, 63}, {294, 64}, {295, 65}, {296, 66}, {297, 67}, {298, 68}, {299, 69}, {300, 70}, {301, 71},
        {302, 72}, {303, 73}, {304, 74}, {305, 75}, {306, 76}, {307, 77}, {308, 78}, {309, 79}, {310, 80},
        {311, 81}, {312, 82}, {313, 83}, {314, 84}, {315, 85}, {316, 86}, {317, 87}, {318, 88}, {319, 89},
        {320, 90}, {321, 91}, {322, 92}, {323, 93}, {324, 95}, {325, 96}, {326, 97}, {327, 98}, {328, 99},
        {329, 100}, {330, 101}, {331, 102}, {332, 103}, {333, 104}, {334, 105}, {335, 106}, {336, 107}, {337, 108},
        {338, 109}, {339, 110}, {340, 111}, {341, 112}, {342, 113}, {343, 114}, {344, 115}, {345, 116}, {346, 117},
        {347, 118}, {348, 119}, {349, 120}, {350, 121}, {351, 122}, {352, 123}, {353, 124}, {354, 125}, {355, 126},
        {356, 127}, {357, 128}, {358, 129}, {359, 130}, {360, 131}, {361, 132}, {362, 133}, {363, 134}, {364, 135},
        {365, 136}, {366, 137}, {367, 138}, {368, 139}, {369, 140}, {370, 141}, {371, 142}, {372, 143}, {373, 144},
        {374, 145}, {375, 146}, {376, 147}, {377, 148}, {378, 149}, {379, 150}, {380, 153}, {381, 154}, {382, 155},
        {383, 156}, {384, 157}, {385, 158}, {386, 159}, {387, 160}, {388, 161}, {389, 162}, {390, 163}, {391, 165},
        {392, 166}, {393, 167}, {394, 169}, {395, 170}, {396, 171}, {397, 172}, {398, 173}, {399, 174}, {400, 176},
        {401, 177}, {402, 178}, {403, 179}, {404, 180}, {405, 181}, {406, 182}, {407, 183}, {408, 184}, {409, 185},
        {410, 186}, {411, 187}, {412, 188}, {413, 189}, {414, 190}, {415, 191}, {416, 192}, {417, 193}, {418, 194},
        {419, 196}, {420, 198}, {421, 201}, {422, 202}, {423, 203}, {424, 204}, {425, 205}, {426, 206}, {427, 207},
        {428, 208}, {429, 209}, {430, 210}, {431, 211}, {432, 212}, {433, 213}, {434, 214}, {435, 215}, {436, 216},
        {437, 217}, {438, 218}, {439, 219}, {440, 220}, {441, 221}, {442, 222}, {443, 223}, {444, 224}, {445, 225},
        {446, 226}, {447, 227}, {448, 228}, {449, 229}, {450, 230}, {451, 231}, {452, 232}, {453, 233}, {454, 234},
        {455, 235}, {456, 236}, {457, 237}, {458, 238}, {459, 239}, {460, 240}, {461, 241}, {462, 242}, {463, 243},
        {464, 244}, {465, 245}, {466, 246}, {467, 247}};

const float fzero = float(0.);
const double padding = 0.1;

const int in_dims = 3;
const int out_dims = 4;
const int num_hands = 2;
const int hand_landmarks_count = 21;
const int two_hands_landmarks_count = num_hands * hand_landmarks_count;
const int face_landmarks_count = 468;
const int hand_coordinates_count = hand_landmarks_count * in_dims;
const int two_hands_coordinates_count = num_hands * hand_coordinates_count;
const int landmarks_count = two_hands_landmarks_count + face_landmarks_count;
const int coordinates_count = landmarks_count * in_dims;

struct Point3D {
    double x, y, z;
};

class Space3D {
public:
    double lower_x = -1.0;
    double upper_x = 1.0;
    double lower_y = -1.0;
    double upper_y = 1.0;
    double lower_z = -1.0;
    double upper_z = 1.0;

    bool is_in_range(struct Point3D point) {
        bool along_x_axis = (lower_x <= point.x) && (point.x <= upper_x);
        bool along_y_axis = (lower_y <= point.y) && (point.y <= upper_y);
        bool along_z_axis = (lower_z <= point.z) && (point.z <= upper_z);
        return (along_x_axis && along_y_axis && along_z_axis);
    }
};

Space3D space;

py::buffer_info check_array_and_get_buffer(const py::array_t<double>& features_array) {
    py::buffer_info buffer = features_array.request();
    if (buffer.ndim != 2 || buffer.shape[0] != landmarks_count || buffer.shape[1] != in_dims)
        throw std::runtime_error("Array must be of shape: (510, 3)");
    return buffer;
}

class ValueRanges {
public:
    double x_min = std::numeric_limits<double>::max();
    double x_max = std::numeric_limits<double>::min();
    double y_min = std::numeric_limits<double>::max();
    double y_max = std::numeric_limits<double>::min();
    double z_min = std::numeric_limits<double>::max();
    double z_max = std::numeric_limits<double>::min();

    void update(double x, double y, double z) {
        x_min = std::fmin(x_min, x);
        x_max = std::fmax(x_max, x);
        y_min = std::fmin(y_min, y);
        y_max = std::fmax(y_max, y);
        z_min = std::fmin(z_min, z);
        z_max = std::fmax(z_max, z);
    }
};

double to_radians(int degrees) {
    return double(degrees) * double(std::atan(1)) / 45;
}

void rotate_3D(struct Point3D &point, int degrees_x, int degrees_y, int degrees_z) {
    double rad, cos, sin;

    degrees_x = degrees_x % 360;
    degrees_y = degrees_y % 360;
    degrees_z = degrees_z % 360;

    if (degrees_x != 0) {
        rad = to_radians(degrees_x);
        cos = std::cos(rad);
        sin = std::sin(rad);
        double y = point.y;
        point.y = cos * y - sin * point.z;
        point.z = sin * y + cos * point.z;
    }
    if (degrees_y != 0) {
        rad = to_radians(degrees_y);
        cos = std::cos(rad);
        sin = std::sin(rad);
        double x = point.x;
        point.x = cos * x + sin * point.z;
        point.z = -sin * x + cos * point.z;
    }
    if (degrees_z != 0) {
        rad = to_radians(degrees_z);
        cos = std::cos(rad);
        sin = std::sin(rad);
        double x = point.x;
        point.x = cos * x - sin * point.y;
        point.y = sin * x + cos * point.y;
    }
}

bool rotate_in_space_3D(
        struct Point3D &point, int degrees_x, int degrees_y, int degrees_z) {
    if (space.is_in_range(point)) {
        if (degrees_x == 0 && degrees_y == 0 && degrees_z == 0) return true;
        rotate_3D(point, degrees_x, degrees_y, degrees_z);
        return space.is_in_range(point);
    }
    return false;
}

float normalize_dist_and_recast(double value) {
    value = std::fmax(0, std::fmin(0.5, value));
    return float(4 * value - 1);
}

float normalize_and_recast(double value) {
    return float(2 * value - 1);
}

double calc_dict_between_points(struct Point3D a, struct Point3D b) {
    double x_dist = b.x - a.x;
    double y_dist = b.y - a.y;
    double z_dist = b.z - a.z;
    double xy_dist_squared = x_dist * x_dist + y_dist * y_dist;
    return std::sqrt(xy_dist_squared + z_dist * z_dist);
}

double scale(double x, double min, double max) {
    return ((x - min) + padding) / (std::abs(min - max) + 2 * padding);
}

void calc_dist_to_face(
        double *input_ptr,
        float *output_ptr,
        ValueRanges& value_ranges,
        int in_idx,
        int out_idx,
        bool do_flip
        ) {
    double x = input_ptr[in_idx];
    double y = input_ptr[in_idx+1];
    double z = input_ptr[in_idx+2];

    if (x < 0 || y < 0) {
        output_ptr[out_idx] = fzero;
        output_ptr[out_idx+1] = fzero;
        output_ptr[out_idx+2] = fzero;
        output_ptr[out_idx+3] = fzero;
    }
    else {
        struct Point3D hand_point = {x, y, z};
        if (do_flip) {
            hand_point.x = 1. - hand_point.x;
        }

        value_ranges.update(x, y, z);

        double min_dist = std::numeric_limits<double>::max();
        for (int j = two_hands_coordinates_count; j < coordinates_count; j += in_dims) {
            struct Point3D face_point = {input_ptr[j], input_ptr[j+1], input_ptr[j+2]};
            if (do_flip) {
                face_point.x = 1. - face_point.x;
            }
            min_dist = std::fmin(min_dist, calc_dict_between_points(hand_point, face_point));
        }
        output_ptr[out_idx+3] = normalize_dist_and_recast(min_dist);
    }
}

void transform(
        double *input_ptr,
        float *output_ptr,
        ValueRanges& value_ranges,
        int in_idx,
        int out_idx,
        bool do_flip,
        int rotate_x,
        int rotate_y,
        int rotate_z
        ) {
    struct Point3D point = {input_ptr[in_idx], input_ptr[in_idx+1], input_ptr[in_idx+2]};

    if (point.x >= 0 && point.y >= 0) {
        if (do_flip) {
            point.x = 1. - point.x;
        }

        point.x = normalize_and_recast(scale(point.x, value_ranges.x_min, value_ranges.x_max));
        point.y = normalize_and_recast(scale(point.y, value_ranges.y_min, value_ranges.y_max));
        point.z = normalize_and_recast(scale(point.z, value_ranges.z_min, value_ranges.z_max));

        if (rotate_in_space_3D(point, rotate_x, rotate_y, rotate_z)) {
            output_ptr[out_idx] = float(point.x);
            output_ptr[out_idx+1] = float(point.y);
            output_ptr[out_idx+2] = float(point.z);
        }
        else {
            output_ptr[out_idx] = fzero;
            output_ptr[out_idx+1] = fzero;
            output_ptr[out_idx+2] = fzero;
            output_ptr[out_idx+3] = fzero;
        }
    }
}

py::array_t<float> pre_process(const py::array_t<double>& features_array) {
    py::buffer_info input_buf = check_array_and_get_buffer(features_array);
    double *input_ptr = static_cast<double *>(input_buf.ptr);

    auto output = py::array_t<float>(two_hands_landmarks_count * out_dims);
    output = output.reshape({two_hands_landmarks_count, out_dims});
    py::buffer_info output_buf = output.request();
    float *output_ptr = static_cast<float *>(output_buf.ptr);

    ValueRanges value_ranges;

    for (int input_idx = 0; input_idx < two_hands_coordinates_count; input_idx += in_dims) {
        int output_idx = input_idx * out_dims / in_dims;
        calc_dist_to_face(input_ptr, output_ptr, value_ranges, input_idx, output_idx, false);
    }

    for (int input_idx = 0; input_idx < two_hands_coordinates_count; input_idx += in_dims) {
        int output_idx = input_idx * out_dims / in_dims;
        transform(input_ptr, output_ptr, value_ranges, input_idx, output_idx, false, 0, 0, 0);
    }

    return output;
}

py::array_t<float> pre_process_training(
        const py::array_t<double>& features_array, bool do_flip, int rotate_x, int rotate_y, int rotate_z) {
    py::buffer_info input_buf = check_array_and_get_buffer(features_array);
    double *input_ptr = static_cast<double *>(input_buf.ptr);

    auto output = py::array_t<float>(out_dims * two_hands_landmarks_count);
    output = output.reshape({two_hands_landmarks_count, out_dims});
    py::buffer_info output_buf = output.request();
    float *output_ptr = static_cast<float *>(output_buf.ptr);

    ValueRanges value_ranges;

    for (int input_idx = 0; input_idx < two_hands_coordinates_count; input_idx += in_dims) {
        int output_idx = input_idx * out_dims / in_dims;
        if (do_flip) {
            if (input_idx < hand_coordinates_count) {
                output_idx = (output_idx + hand_coordinates_count * out_dims / in_dims) %
                             (two_hands_coordinates_count * out_dims / in_dims);
            } else {
                output_idx = (output_idx + hand_coordinates_count * out_dims / in_dims) %
                        (two_hands_coordinates_count * out_dims / in_dims);
            }
        }
        calc_dist_to_face(input_ptr, output_ptr, value_ranges, input_idx, output_idx, do_flip);
    }

    for (int input_idx = 0; input_idx < two_hands_coordinates_count; input_idx += in_dims) {
        int output_idx = input_idx * out_dims / in_dims;
        if (do_flip) {
            if (input_idx < hand_coordinates_count) {
                output_idx = (output_idx + hand_coordinates_count * out_dims / in_dims) %
                             (two_hands_coordinates_count * out_dims / in_dims);
            } else {
                output_idx = (output_idx + hand_coordinates_count * out_dims / in_dims) %
                        (two_hands_coordinates_count * out_dims / in_dims);
            }
        }
        transform(input_ptr, output_ptr, value_ranges, input_idx, output_idx, do_flip, rotate_x, rotate_y, rotate_z);
    }

    return output;
}

PYBIND11_MODULE(dermatillo_pp, m) {
    m.def("pre_process",
          &pre_process,
          "Pre-process hands and face coordinates for a single point in time.",
          py::arg("features_array"));

    m.def("pre_process_training",
          &pre_process_training,
          "Pre-process and transform hands and face coordinates for a single point in time.",
          py::arg("features_array"),
          py::arg("do_flip"),
          py::arg("rotate_x"),
          py::arg("rotate_y"),
          py::arg("rotate_z"));
}
