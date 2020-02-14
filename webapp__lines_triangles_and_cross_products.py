import streamlit as st
import plotly.graph_objects as go
import textwrap

from Qs import add, cross_q, dif, Q, product, rotation_angle, norm_squared

# Sidebar setup.
x_2 = st.sidebar.slider(label="P2_x", min_value=-2.0, max_value=2.0, value=2.0)
y_2 = st.sidebar.slider(label="P2_y", min_value=-2.0, max_value=2.0, value=-2.0)
z_2 = st.sidebar.slider(label="P2_z", min_value=-2.0, max_value=2.0, value=0.0)

o_x = st.sidebar.slider(label="Origin_x", min_value=-2.0, max_value=2.0, value=0.0)
o_y = st.sidebar.slider(label="Origin_y", min_value=-2.0, max_value=2.0, value=0.0)
o_z = st.sidebar.slider(label="Origin_z", min_value=-2.0, max_value=2.0, value=0.0)

if st.sidebar.button("Straighten"):
    x_1 = (x_2 + o_x) / 2
    y_1 = (y_2 + o_y) / 2
    z_1 = (z_2 + o_z) / 2

    st.sidebar.slider(label="P1_x", min_value=-2.0, max_value=2.0, value=x_1)
    st.sidebar.slider(label="P1_y", min_value=-2.0, max_value=2.0, value=y_1)
    st.sidebar.slider(label="P1_z", min_value=-2.0, max_value=2.0, value=z_1)
else:
    x_1 = st.sidebar.slider(label="P1_x", min_value=-2.0, max_value=2.0, value=1.0)
    y_1 = st.sidebar.slider(label="P1_y", min_value=-2.0, max_value=2.0, value=1.0)
    z_1 = st.sidebar.slider(label="P1_z", min_value=-2.0, max_value=2.0, value=1.0)

curvature = st.sidebar.slider(
    label="Curvature", min_value=0.9, max_value=1.0, value=1.0
)
st.sidebar.markdown("TODO: handle traingles with less than 180 degrees")

vertex_p_1 = st.sidebar.checkbox(label="vertex P1", value=False)
vertex_p_2 = st.sidebar.checkbox(label="vertex P2", value=False)
vertex_origin = st.sidebar.checkbox(label="vertex Origin", value=True)

show_code = st.sidebar.checkbox("Show code", False)

# Form points, do the math.
p_1 = Q([0, x_1, y_1, z_1])
p_2 = Q([0, x_2, y_2, z_2])
origin = Q([0, o_x, o_y, o_z])

points = (p_1, p_2, origin)
xs = [p.x for p in points]
ys = [p.y for p in points]
zs = [p.z for p in points]

prod = add(product(dif(p_1, origin), dif(p_2, origin)), origin)

# Cross product
cx_p_1 = add(cross_q(dif(p_2, p_1), dif(origin, p_1)), p_1)
cx_p_2 = add(cross_q(dif(origin, p_2), dif(p_1, p_2)), p_2)
cx_origin = add(product(dif(p_1, origin), dif(p_2, origin), kind="odd"), origin)

# Main page.

st.title("Lines and Triangles")

fig2 = go.Figure()
go.Layout(margin=dict(t=500))
fig2.add_trace(go.Scatter3d(x=[x_1], y=[y_1], z=[z_1], name="P1"))
fig2.add_trace(go.Scatter3d(x=[x_2], y=[y_2], z=[z_2], name="P2"))

fig2.add_trace(go.Mesh3d(x=xs, y=ys, z=zs, color="lightpink", opacity=0.50))

if vertex_p_1:
    fig2.add_trace(
        go.Scatter3d(
            x=[p_1.x, cx_p_1.x],
            y=[p_1.y, cx_p_1.y],
            z=[p_1.z, cx_p_1.z],
            name="P1 cross product",
        )
    )

if vertex_p_2:
    fig2.add_trace(
        go.Scatter3d(
            x=[p_2.x, cx_p_2.x],
            y=[p_2.y, cx_p_2.y],
            z=[p_2.z, cx_p_2.z],
            name="P2 cross product",
        )
    )

if vertex_origin:
    fig2.add_trace(
        go.Scatter3d(
            x=[origin.x, cx_origin.x],
            y=[origin.y, cx_origin.y],
            z=[origin.z, cx_origin.z],
            name="Origin cross product",
        )
    )

st.write(fig2)

angle_p1 = rotation_angle(
    p_2, origin, origin=p_1, tangent_space_norm=curvature, degrees=True
)
angle_p2 = rotation_angle(
    origin, p_1, origin=p_2, tangent_space_norm=curvature, degrees=True
)
angle_origin = rotation_angle(
    p_1, p_2, origin=origin, tangent_space_norm=curvature, degrees=True
)

st.markdown("## Angles")
st.markdown(f"Origin-P1-P2: {angle_p1}")
st.markdown(f"P1-P2-Origin: {angle_p2}")
st.markdown(f"P2-Origin-P1: {angle_origin}")
st.markdown(f"Sum of angles: {round(angle_p1.t + angle_p2.t + angle_origin.t)}")

st.markdown("## Norm Squared Values")

total = norm_squared(prod).t
odd = norm_squared(cx_origin).t

table = f"""Odd | Total
--- | --- | ---
{odd} | {total}"""
st.markdown(f"{table}")

def show_file(label: st, file_name: str, code: bool = False):
    """
    Utility to show contents of a file

    Args:
        label: str
        file_name: str
        code:

    Return: None

    """
    st.markdown("&nbsp ")
    st.markdown(f"### {label}")
    st.write(f"{file_name}")
    with open(f"{file_name}", "r") as file:
        file_lines = file.readlines()

    if code:
        st.code(textwrap.dedent("".join(file_lines[1:])))
    else:
        st.markdown(textwrap.dedent("".join(file_lines[1:])))


st.markdown("""# Quaternion Cross Product

Div, grad, curl, dot product, and cross product were all terms coined by one
individual studying one thing: William Rowan Hamilton in his study of
quaternions. What all students study today is the convenient divorce granted by
Josiah Gibbs. Vector algebra is one of the most useful toolkits in one's
mathematical collection. Vector algebra is such a dominant force in the mind's
eye it may not be possible to imagine different perspectives on the subject. Yet
that is my goal - not to say vector algebra is wrong in any way since there
always necessarily is an equivalence relation between vector algebra and
quaternions. Rather, one may gain new insights based on the the relationships
between terms that are simply not there due to the divorce.

What is a **quaternion cross product**? When one multiplies two quaternion
together, it is the odd part of the product: """)

st.latex("A B = (A B + B A)/2 + (A B - B A)/2 = Even(A B) + Odd(A B)")

st.markdown("Written in component form:")

st.latex("Even(A, B) = (A0 B0 - (A1 B1 + A2 B2 + A3 B3), A0 B1 + A1 B0, A0 B2 + A2 B0, A0 B3 + A3 B0)")

st.latex("Odd(A, B) = (0, A2 B3 - A3 B2, A1 B3 - A3 B1, A1 B2 - A2 B1")

st.markdown("""The quaternions cross product is the odd term. This is not the
standard definition of a Gibbs cross product because there is no notion of the
Even() product which happens to be a combination of the difference of a scalar
times a scalar and vector dot product summed with scalars times vectors
(translation: an abomination to those schooled in vector algebra).

The Gibbs definition of the cross product is the component one without the
zero. Anything one can prove with a Gibbs cross product can be redone using
the quaternion cross product and its zero tag-along.

If one just focuses on the quaternion cross product, the scalar term is always
necessarily equal to zero. Why care about the difference between zero and
undefined as with the Gibb's cross product? One can at least try to think
about zero unlike something that is formally undefined.

In the literture on 3D rotations, the fourth factor is sometimes called "w", 
perhaps a shorthand for what-the-f. As someone who want physics to shape my
mathematics (and visa versa), I think of the scalar as being time, and the
three imaginaries as space. One quaternion represents one event in space-time,
happening now. The cross product can be used to characterize 3 events-now. If
the three events-now are in a line, then the cross product is zero. If the three
events-now are not colinear, then the cross product will not be zero.

Each symmetric or even term involves time. If time gets reversed, the movie
plays backwards but otherwise looks the same. Each anti-symmetric or odd term
is exclusively about space. Spatial reflections use mirrors.

One recent insight is that one quaternion cannot tell a story. Only collections
of quaternions can tell stories. I associate cross products and curls with 
systems changing: a spinning bicycle wheel or a moving eletric field creating
a magnetic field. Each dynamic system is a collection of events, each frame
of the dynamic system happening at time now. The cross product may change
during a succession of nows, from close to being a line to being farther apart.
I look forward to trying to develop analytic animations of such changes.

The angles reported are the same as one expects to see from basic geometry. The
angles sum up to 180 for a flat space-time. I added a curvature slider that
will report on postive curvature, but at this time not negative curvature. There
is always more work to do.

""")

if show_code:
    show_file("Streamlit Webapp code", __file__, code=True)
    show_file("Qs.py library code", "Qs.py", code=True)
