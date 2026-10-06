from flask import (
    Flask,
    jsonify,
    render_template_string,
    request,
    abort,
    redirect,
    make_response
)

app = Flask(__name__)



STUDENTS = {
    "23T1020001": {
        "name": "Nguyễn Văn An",
        "lop": "K47A",
        "scores": {
            "PMNM": 8.5,
            "CSDL": 7.5,
            "HMT": 9.0
        }
    },

    "23T1020002": {
        "name": "Trần Thị Bình",
        "lop": "K47A",
        "scores": {
            "PMNM": 6.0,
            "CSDL": 5.5,
            "HMT": 7.0
        }
    },

    "23T1020003": {
        "name": "Lê Hoàng Cường",
        "lop": "K47B",
        "scores": {
            "PMNM": 9.5,
            "CSDL": 9.0
        }
    },

    "23T1020004": {
        "name": "Phạm Minh Dũng",
        "lop": "K47B",
        "scores": {
            "PMNM": 4.0,
            "CSDL": 3.5,
            "HMT": 5.0
        }
    },

    "23T1020005": {
        "name": "Hoàng Thu Hà",
        "lop": "K47A",
        "scores": {}
    },

    "23T1020006": {
        "name": "Võ Quốc Khánh",
        "lop": "K47C",
        "scores": {
            "PMNM": 7.5,
            "HMT": 8.0
        }
    }
}



def tinh_diem_tb(student):
    scores = student["scores"]

    if not scores:
        return None

    return sum(scores.values()) / len(scores)



def xep_loai(diem):

    if diem is None:
        return "-"

    if diem >= 8:
        return "Giỏi"

    elif diem >= 6.5:
        return "Khá"

    elif diem >= 5:
        return "Trung bình"

    else:
        return "Yếu"



@app.route("/")
def home():

    tong_sinh_vien = len(STUDENTS)

    cac_lop = set()

    for student in STUDENTS.values():
        cac_lop.add(student["lop"])

    tong_lop = len(cac_lop)

    return render_template_string("""
<!DOCTYPE html>

<html lang="vi">

<head>

    <meta charset="UTF-8">

    <title>Quản lý sinh viên</title>

    <style>

        body {
            font-family: Arial;
            margin: 40px;
        }

        h1 {
            color: #333;
        }

        a {
            text-decoration: none;
            color: blue;
        }

    </style>

</head>

<body>

    <h1>QUẢN LÝ SINH VIÊN</h1>

    <p>
        Tổng số sinh viên:
        <b>{{ tong_sinh_vien }}</b>
    </p>

    <p>
        Số lớp:
        <b>{{ tong_lop }}</b>
    </p>

    <hr>

    <h3>Chức năng</h3>

    <p>
        <a href="/students">
            Danh sách sinh viên
        </a>
    </p>

    <p>
        <a href="/search">
            Tìm kiếm sinh viên
        </a>
    </p>

    <p>
        <a href="/api/students">
            API sinh viên
        </a>
    </p>

</body>

</html>
    """,
    tong_sinh_vien=tong_sinh_vien,
    tong_lop=tong_lop
    )



@app.route("/students")
def student_list():

    lop = request.args.get("lop", "").strip()

    if lop == "":
        danh_sach = STUDENTS

    else:

        danh_sach = {}

        for mssv, student in STUDENTS.items():

            if student["lop"].lower() == lop.lower():
                danh_sach[mssv] = student

    cac_lop = sorted(
        set(student["lop"] for student in STUDENTS.values())
    )

    return render_template_string("""
<!DOCTYPE html>

<html lang="vi">

<head>

    <meta charset="UTF-8">

    <title>Danh sách sinh viên</title>

    <style>

        body {
            font-family: Arial;
            margin: 30px;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }

        th, td {
            border: 1px solid #999;
            padding: 10px;
            text-align: center;
        }

        th {
            background-color: #eee;
        }

        a {
            color: blue;
            text-decoration: none;
        }

    </style>

</head>

<body>

    <h1>DANH SÁCH SINH VIÊN</h1>

    <p>
        <a href="/">
            ← Trang chủ
        </a>
    </p>

    <p>
        <b>Lọc theo lớp:</b>

        <a href="/students">
            Tất cả
        </a>

        {% for lop_item in cac_lop %}

            |

            <a href="/students?lop={{ lop_item }}">
                {{ lop_item }}
            </a>

        {% endfor %}

    </p>


    {% if danh_sach %}

    <table>

        <tr>

            <th>MSSV</th>

            <th>Họ tên</th>

            <th>Lớp</th>

            <th>Điểm TB</th>

            <th>Xếp loại</th>

        </tr>


        {% for mssv, student in danh_sach.items() %}

        <tr>

            <td>

                <a href="/students/{{ mssv }}">

                    {{ mssv }}

                </a>

            </td>


            <td>
                {{ student["name"] }}
            </td>


            <td>
                {{ student["lop"] }}
            </td>


            <td>

                {% set diem = tinh_diem_tb(student) %}

                {% if diem is none %}

                    -

                {% else %}

                    {{ "%.2f"|format(diem) }}

                {% endif %}

            </td>


            <td>

                {{ xep_loai(tinh_diem_tb(student)) }}

            </td>

        </tr>

        {% endfor %}

    </table>

    {% else %}

        <p>
            <b>Không có sinh viên phù hợp.</b>
        </p>

    {% endif %}


</body>

</html>
    """,
    danh_sach=danh_sach,
    cac_lop=cac_lop,
    tinh_diem_tb=tinh_diem_tb,
    xep_loai=xep_loai
    )



@app.route("/students/<mssv>")
def student_detail(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=f"Không có sinh viên với MSSV = {mssv}."
        )

    student = STUDENTS[mssv]

    diem_tb = tinh_diem_tb(student)

    loai = xep_loai(diem_tb)

    return render_template_string("""
<!DOCTYPE html>

<html lang="vi">

<head>

    <meta charset="UTF-8">

    <title>Chi tiết sinh viên</title>

    <style>

        body {
            font-family: Arial;
            margin: 30px;
        }

        table {
            border-collapse: collapse;
            width: 600px;
            margin-top: 20px;
        }

        th, td {
            border: 1px solid #999;
            padding: 10px;
            text-align: center;
        }

        th {
            background-color: #eee;
        }

        a {
            color: blue;
            text-decoration: none;
        }

    </style>

</head>

<body>

    <h1>CHI TIẾT SINH VIÊN</h1>


    <p>
        <b>Họ tên:</b>
        {{ student["name"] }}
    </p>


    <p>
        <b>MSSV:</b>
        {{ mssv }}
    </p>


    <p>

        <b>Lớp:</b>

        <a href="/students?lop={{ student['lop'] }}">

            {{ student["lop"] }}

        </a>

    </p>


    <p>

        <b>Điểm TB:</b>

        {% if diem_tb is none %}

            -

        {% else %}

            {{ "%.2f"|format(diem_tb) }}

        {% endif %}

    </p>


    <p>

        <b>Xếp loại:</b>

        {{ loai }}

    </p>


    <h2>Bảng điểm từng học phần</h2>


    {% if student["scores"] %}

    <table>

        <tr>

            <th>Học phần</th>

            <th>Điểm</th>

        </tr>


        {% for hoc_phan, diem in student["scores"].items() %}

        <tr>

            <td>
                {{ hoc_phan }}
            </td>

            <td>
                {{ diem }}
            </td>

        </tr>

        {% endfor %}

    </table>

    {% else %}

        <p>
            Chưa có điểm.
        </p>

    {% endif %}


    <p>

        <a href="/students/{{ mssv }}/export">

            Tải bảng điểm (CSV)

        </a>

    </p>


    <p>

        <a href="/sv/{{ mssv }}">

            Link rút gọn

        </a>

    </p>


    <p>

        <a href="/students">

            ← Danh sách sinh viên

        </a>

    </p>

</body>

</html>
    """,
    mssv=mssv,
    student=student,
    diem_tb=diem_tb,
    loai=loai
    )


@app.route("/sv/<mssv>")
def short_student(mssv):

    return redirect(
        f"/students/{mssv}",
        code=301
    )


@app.route("/students/<mssv>/export")
def export_csv(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=f"Không có sinh viên với MSSV = {mssv}."
        )

    student = STUDENTS[mssv]

    # Nội dung CSV
    lines = []

    lines.append("hoc_phan,diem")

    for hoc_phan, diem in student["scores"].items():

        lines.append(
            f"{hoc_phan},{diem}"
        )

    csv_content = "\n".join(lines)

    # Tạo response
    response = make_response(csv_content)

    response.headers["Content-Type"] = (
        "text/csv; charset=utf-8"
    )

    response.headers["Content-Disposition"] = (
        f"attachment; filename=diem_{mssv}.csv"
    )

    return response


@app.route("/search")
def search():

    q = request.args.get("q", "")

    keyword = q.strip()

    ket_qua = []

    if keyword != "":

        keyword_lower = keyword.casefold()

        for mssv, student in STUDENTS.items():

            if (
                keyword_lower in student["name"].casefold()
                or keyword_lower in mssv.casefold()
            ):

                ket_qua.append(
                    (mssv, student)
                )


    return render_template_string("""
<!DOCTYPE html>

<html lang="vi">

<head>

    <meta charset="UTF-8">

    <title>Tìm kiếm sinh viên</title>

    <style>

        body {
            font-family: Arial;
            margin: 30px;
        }

        input {
            padding: 8px;
            width: 300px;
        }

        button {
            padding: 8px 15px;
        }

        li {
            margin: 10px 0;
        }

        a {
            color: blue;
            text-decoration: none;
        }

    </style>

</head>

<body>


    <h1>TÌM KIẾM SINH VIÊN</h1>


    <form method="GET" action="/search">

        <input
            type="text"
            name="q"
            value="{{ keyword }}"
            placeholder="Nhập họ tên hoặc MSSV"
        >

        <button type="submit">
            Tìm kiếm
        </button>

    </form>


    {% if keyword %}

        <h3>

            Tìm thấy {{ ket_qua|length }}
            kết quả cho "{{ keyword }}"

        </h3>


        {% if ket_qua %}

        <ul>

            {% for mssv, student in ket_qua %}

            <li>

                <a href="/students/{{ mssv }}">

                    {{ student["name"] }}

                    - {{ mssv }}

                </a>

            </li>

            {% endfor %}

        </ul>

        {% else %}

            <p>
                Không tìm thấy sinh viên.
            </p>

        {% endif %}

    {% endif %}


    <p>

        <a href="/">
            ← Trang chủ
        </a>

    </p>


</body>

</html>
    """,
    keyword=keyword,
    ket_qua=ket_qua
    )


@app.route("/api/students")
def api_students():

    return jsonify(STUDENTS)


if __name__ == "__main__":

    app.run(
        debug=True,
        port=8000
    )