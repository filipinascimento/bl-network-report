<h1 align="center">Network Report</h1>

<p align="center">
  Generates an HTML report for a network (JGF), with a table of network properties and histograms of network and node attributes, optionally compared with null-model distributions, using igraph.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.435"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.435-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-see_LICENSE-lightgrey.svg" alt="License"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Generates an HTML report for a network (JGF), with a table of network properties and histograms of network and node attributes, optionally compared with null-model distributions, using igraph.**

Loads the first network of a JSON Graph Format file with igraph (by default keeping only the giant connected component), tabulates its network-level properties and plots distributions of network and node attributes as PNG and PDF figures embedded in an HTML page. If a null-model network is given, its average distributions are drawn for comparison. Use it to inspect connectivity networks produced by other brainlife network Apps.

| | |
|---|---|
| **Inputs** | `generic/network` · `generic/network` (optional) |
| **Outputs** | `report/html` |
| **Container** | `filsilva/cxnetwork:0.2.0` |
| **Resources** | 1 CPUs |
| **Run it** | [doi.org/10.25663/brainlife.app.435](https://doi.org/10.25663/brainlife.app.435) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `network` | `generic/network` | yes | Input network used to generate a report. |
| `nullmodels` | `generic/network` (null-model) | no | Null model to be used as comparison for the distributions. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `output` | `report/html` | Report of the network, with plots and tables describing network properties. |

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.435](https://doi.org/10.25663/brainlife.app.435), choose `generic/network`, `generic/network` from your project and press **Execute**. The results are saved to your project as `report/html`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `filsilva/cxnetwork:0.2.0`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "network": "/path/to/network/network",
       "nullmodels": "/path/to/nullmodels/nullmodels"
   }
   ```

3. Run `./main`.

## Troubleshooting

- **The network file should contain at least one network.**: Provide a JGF file containing at least one network.

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- Network Report. brainlife.io App. [doi:10.25663/brainlife.app.435](https://doi.org/10.25663/brainlife.app.435)
- Bassett D. S., Sporns O. Network neuroscience. Nature Neuroscience 20(3):353 (2017). [doi:10.1038/nn.4502](https://doi.org/10.1038/nn.4502)
- Costa L. da F., Rodrigues F. A., Travieso G., Villas Boas P. R. Characterization of complex networks: A survey of measurements. Advances in Physics 56(1):167-242 (2007).
- Costa, L. da F., Francisco A. Rodrigues, Gonzalo Travieso, and Paulino Ribeiro Villas Boas. "Characterization of complex networks: A survey of measurements." Advances in physics 56, no. 1 (2007): 167-242.[https://doi.org/10.1080/00018730601170527](https://doi.org/10.1080/00018730601170527)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- [Filipi N. Silva](https://filipinascimento.github.io)

**Contributors**

- [Franco Pestilli](https://liberalarts.utexas.edu/psychology/faculty/fp4834)

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io, which runs this App, is publicly funded by Wellcome, the U.S. National Institutes of Health and the U.S. National Science Foundation; acknowledging that support helps keep it running.</sub>

## License

See [LICENSE](LICENSE).
