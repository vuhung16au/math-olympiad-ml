#!/usr/bin/env node

/**
 * Thumbnail Generation Script for HSC Math Hub
 * Generates thumbnail images from the first page of each PDF
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const { spawn } = require('child_process');

// Import booklets data (using require with path resolution)
const booklets = [
  {
    id: "hsc-collections",
    title: "HSC Collections",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Collections/releases/HSC-Collections.pdf",
    outputFile: "hsc-collections.png",
  },
  {
    id: "hsc-combinatorics",
    title: "HSC Combinatorics",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Combinatorics/releases/HSC-Combinatorics.pdf",
    outputFile: "hsc-combinatorics.png",
  },
  {
    id: "hsc-complex-numbers",
    title: "HSC Complex Numbers",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-ComplexNumbers/releases/HSC-ComplexNumbers.pdf",
    outputFile: "hsc-complex-numbers.png",
  },
  {
    id: "hsc-distributions",
    title: "HSC Distributions",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Distributions/releases/HSC-Distributions.pdf",
    outputFile: "hsc-distributions.png",
  },
  {
    id: "hsc-functions",
    title: "HSC Functions",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Functions/releases/HSC-Functions.pdf",
    outputFile: "hsc-functions.png",
  },
  {
    id: "hsc-induction",
    title: "HSC Induction",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Induction/releases/HSC-Induction.pdf",
    outputFile: "hsc-induction.png",
  },
  {
    id: "hsc-inequalities",
    title: "HSC Inequalities",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Inequalities/releases/HSC-Inequalities.pdf",
    outputFile: "hsc-inequalities.png",
  },
  {
    id: "hsc-integrals",
    title: "HSC Integrals",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Integrals/releases/HSC-Integrals.pdf",
    outputFile: "hsc-integrals.png",
  },
  {
    id: "hsc-last-resorts",
    title: "HSC Last Resorts",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-LastResorts/releases/HSC-LastResorts.pdf",
    outputFile: "hsc-last-resorts.png",
  },
  {
    id: "hsc-math-extension-2-book",
    title: "HSC Math Extension 2 Book",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Math-Extension-2-Book/releases/HSC-Math-Extension-2-Book.pdf",
    outputFile: "hsc-math-extension-2-book.png",
  },
  {
    id: "hsc-mechanics",
    title: "HSC Mechanics",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Mechanics/releases/HSC-Mechanics.pdf",
    outputFile: "hsc-mechanics.png",
  },
  {
    id: "hsc-polynomials",
    title: "HSC Polynomials",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Polynomials/releases/HSC-Polynomials.pdf",
    outputFile: "hsc-polynomials.png",
  },
  {
    id: "hsc-polynomials-extension1",
    title: "HSC Polynomials Extension 1",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Polynomials-Extension1/releases/HSC-Polynomials-Extension1.pdf",
    outputFile: "hsc-polynomials-extension1.png",
  },
  {
    id: "hsc-probability",
    title: "HSC Probability",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Probability/releases/HSC-Probability.pdf",
    outputFile: "hsc-probability.png",
  },
  {
    id: "hsc-proofs",
    title: "HSC Proofs",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Proofs/releases/HSC-Proofs.pdf",
    outputFile: "hsc-proofs.png",
  },
  {
    id: "hsc-trigonometry",
    title: "HSC Trigonometry",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Trigonometry/releases/HSC-Trigonometry.pdf",
    outputFile: "hsc-trigonometry.png",
  },
  {
    id: "hsc-vectors",
    title: "HSC Vectors",
    pdfUrl: "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Vectors/releases/HSC-Vectors.pdf",
    outputFile: "hsc-vectors.png",
  },
];

const THUMBNAIL_DIR = path.join(__dirname, '../public/thumbnails');
const TEMP_DIR = path.join(__dirname, '../.temp-pdfs');

// Ensure directories exist
if (!fs.existsSync(THUMBNAIL_DIR)) {
  fs.mkdirSync(THUMBNAIL_DIR, { recursive: true });
}

if (!fs.existsSync(TEMP_DIR)) {
  fs.mkdirSync(TEMP_DIR, { recursive: true });
}

/**
 * Download PDF from URL
 */
async function downloadPdf(url, outputPath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(outputPath);
    https.get(url, (response) => {
      if (response.statusCode !== 200) {
        reject(new Error(`Failed to download: HTTP ${response.statusCode}`));
        return;
      }
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
    }).on('error', (err) => {
      fs.unlink(outputPath, () => {});
      reject(err);
    });
  });
}

/**
 * Convert first page of PDF to PNG using ImageMagick/Ghostscript
 */
async function convertPdfToImage(pdfPath, outputPath) {
  return new Promise((resolve, reject) => {
    // Using ImageMagick's convert command
    // Converts first page of PDF to PNG at 300 DPI
    const proc = spawn('convert', [
      `${pdfPath}[0]`,  // First page only
      '-density', '150',
      '-quality', '80',
      '-resize', '480x640',
      outputPath
    ]);

    proc.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`ImageMagick convert failed with code ${code}`));
      }
    });

    proc.on('error', (err) => {
      reject(err);
    });
  });
}

/**
 * Main thumbnail generation function
 */
async function generateThumbnails() {
  console.log('🎬 Starting thumbnail generation...\n');

  let successCount = 0;
  let failedCount = 0;

  for (const booklet of booklets) {
    try {
      console.log(`📖 Processing: ${booklet.title}...`);

      const pdfPath = path.join(TEMP_DIR, `${booklet.id}.pdf`);
      const thumbnailPath = path.join(THUMBNAIL_DIR, booklet.outputFile);

      // Download PDF
      process.stdout.write('  ↓ Downloading PDF... ');
      await downloadPdf(booklet.pdfUrl, pdfPath);
      console.log('✓');

      // Convert to thumbnail
      process.stdout.write('  ⚙ Converting to image... ');
      await convertPdfToImage(pdfPath, thumbnailPath);
      console.log('✓');

      // Clean up temp PDF
      fs.unlinkSync(pdfPath);

      console.log(`  ✓ Saved to: ${booklet.outputFile}\n`);
      successCount++;

    } catch (error) {
      console.error(`  ✗ Error: ${error.message}\n`);
      failedCount++;
    }
  }

  // Clean up temp directory
  try {
    fs.rmSync(TEMP_DIR, { recursive: true, force: true });
  } catch {
    // Ignore cleanup errors
  }

  // Summary
  console.log('━'.repeat(50));
  console.log(`✓ Successfully generated: ${successCount} thumbnails`);
  if (failedCount > 0) {
    console.log(`✗ Failed: ${failedCount} thumbnails`);
  }
  console.log('━'.repeat(50));

  if (failedCount === 0) {
    console.log('\n✅ All thumbnails generated successfully!');
    console.log(`📁 Saved to: ${THUMBNAIL_DIR}\n`);
  } else {
    console.log(`\n⚠️  Some thumbnails failed. Check errors above.\n`);
    process.exit(1);
  }
}

// Run
generateThumbnails().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
