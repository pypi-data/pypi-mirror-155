import matplotlib.pyplot as plt

c = "#426174"
w = 4.00
r = 1.25
dpi = 300

fig, ax = plt.subplots()
ax.set_ylim(-2, 4)
ax.set_xlim(-2, 3 * w + 2)
ax.set_aspect("equal", "box")
ax.set_axis_off()

# draw 4 'o's
for i in range(4):
    ax.add_patch(plt.Circle((i * w, 0), 2, color=c, lw=0))
    ax.add_patch(plt.Circle((i * w, 0), r, color="w", lw=0))

# ---- b ----
ax.add_patch(plt.Rectangle((-2, 0), 2 - r, 4, color=c, lw=0))
# ---- o ----
# ---- l ----
ax.add_patch(plt.Rectangle((2 * w - 2, 0), 4, 4, color="w", lw=0))
ax.add_patch(plt.Rectangle((2 * w - 2, -0.05), 2 - r, 4, color=c, lw=0))
# ---- a ----
ax.add_patch(plt.Rectangle((3 * w + r, 0), 2 - r, -2, color=c, lw=0))

fig.savefig("bola.svg", bbox_inches="tight")
plt.show()
