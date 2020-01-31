import streamlit as sl
from Qs import *
import plotly.graph_objects as go

# Sidebar setup.
x_1 = sl.sidebar.slider(label="P1_x", min_value=-2.0, max_value=2.0, value=1.0)
y_1 = sl.sidebar.slider(label="P1_y", min_value=-2.0, max_value=2.0, value=1.0)
z_1 = sl.sidebar.slider(label="P1_z", min_value=-2.0, max_value=2.0, value=1.0)
p_1 = Qs([0, x_1, y_1, z_1])

x_2 = sl.sidebar.slider(label="P2_x", min_value=-2.0, max_value=2.0, value=2.0)
y_2 = sl.sidebar.slider(label="P2_y", min_value=-2.0, max_value=2.0, value=-2.0)
z_2 = sl.sidebar.slider(label="P2_z", min_value=-2.0, max_value=2.0, value=0.0)
p_2 = Qs([0, x_2, y_2, z_2])

o_x = sl.sidebar.slider(label="Origin_x", min_value=-2.0, max_value=2.0, value=0.0)
o_y = sl.sidebar.slider(label="Origin_y", min_value=-2.0, max_value=2.0, value=0.0)
o_z = sl.sidebar.slider(label="Origin_z", min_value=-2.0, max_value=2.0, value=0.0)
origin = Qs([0, o_x, o_y, o_z])

curvature = sl.sidebar.slider(
    label="Curvature", min_value=0.9, max_value=1.1, value=1.0
)

vertex_p_1 = sl.sidebar.checkbox(label="vertex P1", value=False)
vertex_p_2 = sl.sidebar.checkbox(label="vertex P2", value=False)
vertex_origin = sl.sidebar.checkbox(label="vertex Origin", value=True)

points = (p_1, p_2, origin)
xs = [p.x for p in points]
ys = [p.y for p in points]
zs = [p.z for p in points]

prod = product(dif(p_1, origin), dif(p_2, origin))

# Cross product
cx_p_1 = add(cross_q(dif(p_2, p_1), dif(origin, p_1)), p_1)
cx_p_2 = add(cross_q(dif(origin, p_2), dif(p_1, p_2)), p_2)
cx_origin = add(cross_q(dif(p_1, origin), dif(p_2, origin)), origin)

sl.title("Lines and Triangles")

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

sl.write(fig2)

angle_p1 = rotation_angle(
    p_2, origin, origin=p_1, tangent_space_norm=curvature, degrees=True
)
angle_p2 = rotation_angle(
    origin, p_1, origin=p_2, tangent_space_norm=curvature, degrees=True
)
angle_origin = rotation_angle(
    p_1, p_2, origin=origin, tangent_space_norm=curvature, degrees=True
)

sl.markdown("## Angles")
sl.markdown(f"Origin-P1-P2: {angle_p1}")
sl.markdown(f"P1-P2-Origin: {angle_p2}")
sl.markdown(f"P2-Origin-P1: {angle_origin}")
sl.markdown(f"Sum of angles: {round(angle_p1.t + angle_p2.t + angle_origin.t)}")

sl.markdown("## Norm Squared Values")
sl.markdown(f"P1 * P2: {norm_squared(prod).t}")
sl.markdown(f"P1 X P2: {norm_squared(cx_origin).t}")
