# Quiqup Terms of Service Page - Design Parameters

Source URL: https://www.quiqup.com/terms-of-service/full-cross-border-quiqup-services-and-fees-schedule---self-service-24-11-01

---

## Typography

| Property | Value |
|----------|-------|
| **Font Family** | `"DM Sans", sans-serif` |
| **Google Fonts** | `https://fonts.googleapis.com/css?family=DM+Sans:300,400,500,600,700` |
| **Font Weights** | 300, 400, 500, 600, 700 |

### Font Sizes
| Usage | Size |
|-------|------|
| Hero/Display | 96px |
| Large Heading | 48px, 46.4px |
| Section Heading | 24px |
| Subheading | 20px |
| Body Large | 17.6px |
| Body | 16px |
| Body Small | 14px |
| Caption | 12.8px, 12px |
| Micro | 9.6px |

### Line Heights
- 115.2px (for 96px text)
- 48px, 46.4px (for large headings)
- 35.2px, 33.6px (for medium headings)
- 28px, 24px (for body text)
- 21px, 19.2px (for small text)

---

## Color Palette

### Brand Colors
| Name | RGB | Hex | Usage |
|------|-----|-----|-------|
| Brand Primary (Dark Purple) | `rgb(35, 0, 91)` | `#23005B` | Headers, footer, CTAs |
| Brand Accent (Bright Purple) | `rgb(108, 101, 247)` | `#6C65F7` | Links, accents |
| Brand Yellow | `rgb(255, 209, 0)` | `#FFD100` | Highlights, accents |

### Text Colors
| Name | RGB | Hex | Usage |
|------|-----|-----|-------|
| Text Primary | `rgb(0, 0, 0)` | `#000000` | Main body text |
| Text Secondary | `rgb(51, 51, 51)` | `#333333` | Secondary text |
| Text Light | `rgb(244, 244, 244)` | `#F4F4F4` | Text on dark backgrounds |
| Text White | `rgb(255, 255, 255)` | `#FFFFFF` | Text on dark backgrounds |

### Background Colors
| Name | RGB | Hex | Usage |
|------|-----|-----|-------|
| Page Background | `rgb(244, 246, 252)` | `#F4F6FC` | Main page background |
| Section Gray | `rgb(244, 244, 244)` | `#F4F4F4` | Alternate sections |
| Dark Background | `rgb(35, 0, 91)` | `#23005B` | Footer, banners |
| White | `rgb(255, 255, 255)` | `#FFFFFF` | Cards, content areas |

---

## CSS Variables

```css
:root {
  /* Brand Colors */
  --brand-primary: #23005B;
  --brand-accent: #6C65F7;
  --brand-yellow: #FFD100;

  /* Text Colors */
  --text-primary: #000000;
  --text-secondary: #333333;
  --text-light: #F4F4F4;
  --text-white: #FFFFFF;

  /* Background Colors */
  --bg-page: #F4F6FC;
  --bg-section: #F4F4F4;
  --bg-dark: #23005B;
  --bg-white: #FFFFFF;

  /* Typography */
  --font-family: "DM Sans", sans-serif;
  --font-weight-light: 300;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Font Sizes */
  --text-display: 96px;
  --text-h1: 48px;
  --text-h2: 46.4px;
  --text-h3: 24px;
  --text-h4: 20px;
  --text-body-lg: 17.6px;
  --text-body: 16px;
  --text-body-sm: 14px;
  --text-caption: 12px;
  --text-micro: 9.6px;

  /* Line Heights */
  --leading-display: 115.2px;
  --leading-h1: 48px;
  --leading-h3: 35.2px;
  --leading-body: 28px;
  --leading-tight: 24px;
  --leading-small: 21px;
}
```

---

## Page Structure

1. **Header/Navigation**
   - Fixed navigation bar
   - Logo on left
   - Navigation links on right

2. **Hero Section**
   - Title: "Quiqup Services and Fees Schedule"
   - Subtitle with terms link
   - Light background (#F4F6FC)

3. **Services Section**
   - "UAE Delivery Services" heading
   - Pricing tables with columns
   - Light gray borders

4. **Coverage Areas**
   - "Coverage Area by Service" heading
   - Regional zones with embedded images
   - Delivery schedule tables

5. **Banner Section**
   - Dark purple background (#23005B)
   - Large white text tagline
   - "Quiqup is your modern fulfilment partner in the UAE"

6. **Footer**
   - Dark purple background (#23005B)
   - Logo watermark
   - Social media icons (Facebook, Instagram, X/Twitter, LinkedIn)
   - Navigation links in columns
   - Copyright text
   - Legal links (Privacy Policy, Terms of Service)

---

## Additional Notes

- Anti-aliasing enabled: `-webkit-font-smoothing: antialiased`
- Built with Webflow
- Responsive images with srcset
- Tables use simple borders with rgba(0, 0, 0, 0.47) for subtle effect
