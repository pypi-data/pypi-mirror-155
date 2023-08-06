"""Command-line interface."""
import os

import click
import matplotlib as mpl
import numpy as np
import skimage  # type: ignore
import tifffile  # type: ignore
from matplotlib.backends import backend_pdf  # type: ignore
from scipy import ndimage  # type: ignore

from nima import nima
from nima import scripts


@click.command()
@click.version_option()
@click.option("--silent", is_flag=True, help="Do not print; verbose=0.")
@click.option(
    "-o",
    "--output",
    type=str,
    default="nima",
    help="Output folder path [default:nima].",
)
@click.option(
    "--hotpixels",
    is_flag=True,
    default=False,
    help="Median filter (rad=0.5) to remove hotpixels.",
)
@click.option("-f", "--flat", type=str, help="Dark for shading correction.")
@click.option("-d", "--dark", type=str, help="Flat for shading correction.")
@click.option(
    "--bg-method",
    type=click.Choice(
        ["li_adaptive", "entropy", "arcsinh", "adaptive", "li_li"], case_sensitive=False
    ),
    default="li_adaptive",
    prompt_required=False,
    prompt=True,
    help="Background estimation algorithm [default:li_adaptive].",
)
@click.option("--bg-downscale", type=(int, int), help="Binning Y X.")
@click.option(
    "--bg-radius", type=float, help="Radius for entropy or arcsinh methods [def:10]."
)
@click.option(
    "--bg-adaptive-radius", type=float, help="Radius for adaptive methods [def:X/2]."
)
@click.option(
    "--bg-percentile",
    type=float,
    help="Percentile for entropy or arcsinh methods [def:10].",
)
@click.option(
    "--bg-percentile-filter",
    type=float,
    help="Percentile filter for arcsinh method [def:80].",
)
@click.option(
    "--fg-method",
    type=click.Choice(["yen", "li"], case_sensitive=False),
    default="yen",
    prompt_required=False,
    prompt=True,
    help="Segmentation algorithm [default:yen].",
)
@click.option("--min-size", type=float, help="Minimum size labeled objects [def:2000].")
@click.option(
    "--clear-border", is_flag=True, help="Remove labels touching image borders."
)
@click.option("--wiener", is_flag=True, help="Wiener filter before segmentation.")
@click.option(
    "--watershed", is_flag=True, help="Watershed binary mask (to label cells)."
)
@click.option(
    "--randomwalk", is_flag=True, help="Randomwalk binary mask (to label cells)."
)
#
@click.option(
    "--image-ratios/--no-image-ratios",
    default=True,
    help="Compute ratio images? [default:True]",
)
@click.option(
    "--ratio-median-radii",
    type=str,
    help="Median filter ratio images with radii [def:(7,3)].",
)
@click.option(
    "--channels-cl",
    type=(str, str),
    default=("C", "R"),
    help="Channels for Cl ratio [default:C/R].",
)
@click.option(
    "--channels-ph",
    type=(str, str),
    default=("G", "C"),
    help="Channels for pH ratio [default:G/C].",
)
# # TODO: @click.argument("tiffstk", type=click.File("r"))
@click.argument("tiffstk", type=str)
# @click.argument("channels", type=list[str], default=["G", "R", "C"])
@click.argument("channels", type=str, nargs=-1)
def main(  # type: ignore
    silent,
    output,
    hotpixels,
    flat,
    dark,
    fg_method,
    min_size,
    clear_border,
    wiener,
    watershed,
    randomwalk,
    bg_method,
    bg_downscale,
    bg_radius,
    bg_adaptive_radius,
    bg_percentile,
    bg_percentile_filter,
    image_ratios,
    ratio_median_radii,
    channels_cl,
    channels_ph,
    tiffstk,
    channels,
):
    """Analyze multichannel (default:["G", "R", "C"]) tiff time-lapse stack.

    TIFFSTK  :  Image file.

    CHANNELS :  Channel names.

    Save:
    (1) representation of image channels and segmentation ``BN_dim.png``,
    (2) plot of ratios and channel intensities for each label and bg vs.
    time ``BN_meas.png``,
    (3) table of bg values ``*/bg.csv``,
    (4) representation of bg image and histogram at all time points for
    each channel ``BN/bg-[C1,C2,⋯]-method.pdf``, and for each label:
    (5) table of ratios and measured properties ``BN/label[1,2,⋯].csv``
    and (6) ratio images ``BN/label[1,2,⋯]_r[cl,pH].tif``.
    """
    click.echo(tiffstk)
    channels = ("G", "R", "C") if len(channels) == 0 else channels
    click.echo(channels)
    d_im, _, t = nima.read_tiff(tiffstk, channels)
    if not silent:
        print("  Times: ", t)
    if hotpixels:
        d_im = nima.d_median(d_im)
    if flat:
        # XXX: this is imperfect: dark must be present of flat
        dark, _, _ = nima.read_tiff(dark, channels)
        flat, _, _ = nima.read_tiff(flat, channels)
        d_im = nima.d_shading(d_im, dark, flat, clip=True)
    kwargs_bg = {"kind": bg_method}
    if bg_downscale:
        kwargs_bg["downscale"] = bg_downscale
    if bg_radius:
        kwargs_bg["radius"] = bg_radius
    if bg_adaptive_radius:
        kwargs_bg["adaptive_radius"] = bg_adaptive_radius
    if bg_percentile:
        kwargs_bg["perc"] = bg_percentile
    if bg_percentile_filter:
        kwargs_bg["arcsinh_perc"] = bg_percentile_filter
    click.echo(kwargs_bg)
    d_im_bg, bgs, ff, _bgv = nima.d_bg(d_im, **kwargs_bg)  # clip=True
    print(bgs)

    kwargs_mask_label = {"channels": channels, "threshold_method": fg_method}
    if min_size:
        kwargs_mask_label["min_size"] = min_size
    if clear_border:
        kwargs_mask_label["clear_border"] = True
    if wiener:
        kwargs_mask_label["wiener"] = True
    if watershed:
        kwargs_mask_label["watershed"] = True
    if randomwalk:
        kwargs_mask_label["randomwalk"] = True
    click.secho(kwargs_mask_label)
    nima.d_mask_label(d_im_bg, **kwargs_mask_label)
    kwargs_meas_props = {"channels": channels}
    kwargs_meas_props["ratios_from_image"] = image_ratios
    if ratio_median_radii:
        kwargs_meas_props["radii"] = tuple(
            int(r) for r in ratio_median_radii.split(",")
        )
    click.secho(kwargs_meas_props)
    meas, pr = nima.d_meas_props(
        d_im_bg, channels_cl=channels_cl, channels_ph=channels_ph, **kwargs_meas_props
    )
    #     # output for bg
    bname = os.path.basename(tiffstk)
    bname = os.path.splitext(bname)[0]
    bname = os.path.join(output, bname)
    if not os.path.exists(bname):
        os.makedirs(bname)
    bname_bg = os.path.join(bname, "bg")
    for ch, llf in ff.items():
        pp = backend_pdf.PdfPages(bname_bg + "-" + ch + "-" + bg_method + ".pdf")
        for lf in llf:
            for f_i in lf:
                pp.savefig(f_i)  # e.g. entropy output 2 figs
        pp.close()
    column_order = ["C", "G", "R"]  # FIXME must be equal anyway in testing
    bgs[column_order].to_csv(bname_bg + ".csv")
    # TODO: plt.close('all') or control mpl warning
    # output for fg (target)
    f = nima.d_plot_meas(bgs, meas, channels=channels)
    f.savefig(bname + "_meas.png")
    ##
    # show all channels and labels only.
    d = {ch: d_im_bg[ch] for ch in channels}
    d["labels"] = d_im_bg["labels"]
    f = nima.d_show(d, cmap=mpl.cm.inferno_r)  # type: ignore
    f.savefig(bname + "_dim.png")
    ##
    # meas csv
    for k, df in meas.items():
        column_order = [
            "C",
            "G",
            "R",
            "area",
            "eccentricity",
            "equivalent_diameter",
            "r_cl",
            "r_pH",
            "r_cl_median",
            "r_pH_median",
        ]
        df[column_order].to_csv(os.path.join(bname, "label" + str(k) + ".csv"))
    # ##
    # labelX_{rcl,rpH}.tif ### require r_cl and r_pH present in d_im
    objs = ndimage.find_objects(d_im_bg["labels"])
    for n, o in enumerate(objs):
        name = os.path.join(bname, "label" + str(n + 1) + "_rcl.tif")
        tifffile.imwrite(name, d_im_bg["r_cl"][o], compression="lzma")
        name = os.path.join(bname, "label" + str(n + 1) + "_rpH.tif")
        tifffile.imwrite(name, d_im_bg["r_pH"][o], compression="lzma")


@click.group()
@click.version_option()
def bias():  # type: ignore
    """Help preparing files for flat correction.

    New: DARK and FLAT are a single file, and both must be a d_im with appropriate
    channels.
    """
    pass


@bias.command()
@click.argument("zipfile", type=str)
def dark(zipfile):  # type: ignore
    """Prepare Dark image file.

    It reads a stack of dark images (tiff-zip) and save (in current dir):
    - DARK image = median filter of median projection.
    - plot (histograms, median, projection, hot pixels).
    - csv file containing coordinates of hotpixels.
    """
    dark_im, dark_hotpixels, f = scripts.dark(zipfile)
    click.secho("DARK", bold=True, fg="red")
    # output
    bname = "dark-" + os.path.splitext(os.path.basename(zipfile))[0]
    f.savefig(bname + ".pdf")
    # TODO suppress UserWarning low contrast is actually expected here
    skimage.io.imrite(bname + ".tif", dark_im, plugin="tifffile")
    dark_hotpixels.to_csv(bname + ".csv")
    print("median [ IQR ] = ", np.median(dark_im), np.percentile(dark_im, [25, 75]))


@bias.command()
@click.argument("darkfile", type=str)
@click.argument("zipfile", type=str)
def flat(darkfile, zipfile):  # type: ignore
    """Prepare Flat image file.

    Reads a stack of flat images (tiff-zip) and a DARK reference image, and save (in pwd):
    - FLAT image = median filter of median projection.
    - plot (stack histograms, flat image and its histogram - name of stack and
    reference dark image)
    """
    click.secho("FLAT", bold=True, fg="yellow")
    flat_im, f = scripts.flat(zipfile, darkfile)
    # output
    bname = (
        "flat-"
        + os.path.splitext(os.path.basename(zipfile))[0]
        + "-"
        + os.path.splitext(os.path.basename(darkfile))[0]
    )
    f.savefig(bname + ".pdf")
    skimage.io.imwrite(bname + ".tif", flat_im)


if __name__ == "__main__":
    main(prog_name="dimg")  # pragma: no cover
