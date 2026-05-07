import * as cheerio from "cheerio";

function repairKnownMake4htArtifacts(html: string) {
  return html
    .replaceAll(
      /<span class=['"]cmmi-[^'"]+['"]>\/span&gt;\s*<img/gi,
      "&lt; <img",
    )
    .replaceAll(
      /<span class=['"]cmmi-[^'"]+['"]>&lt;\/span&gt;\s*<img/gi,
      "&lt; <img",
    )
    .replaceAll(
      /<span class=['"]cmmi-[^'"]+['"]>&gt;\/span&gt;\s*<img/gi,
      "&gt; <img",
    )
    .replaceAll(
      /(<span class=['"]cmmi-[^'"]+['"]>[^<]+?)\s*&lt;\/span&gt;/gi,
      "$1</span> &lt;",
    )
    .replaceAll(
      /(<span class=['"]cmmi-[^'"]+['"]>[^<]+?)\s*&gt;\/span&gt;/gi,
      "$1</span> &gt;",
    )
    .replaceAll(
      /(<\/sub>)\s*<span class=['"]cmmi-[^'"]+['"]>\/span&gt;\s*/gi,
      "$1 &lt; ",
    )
    .replaceAll(
      /(<\/sub>)\s*<span class=['"]cmmi-[^'"]+['"]>&gt;\/span&gt;\s*/gi,
      "$1 &gt; ",
    );
}

function rewriteAssetUrl(src: string, slug: string) {
  if (
    src.startsWith("http://") ||
    src.startsWith("https://") ||
    src.startsWith("data:") ||
    src.startsWith("/")
  ) {
    return src;
  }

  return `/_generated/assets/${slug}/${src.replace(/^\.\//, "")}`;
}

function normalizeWhitespace(text: string) {
  return text.replace(/\u00a0/g, " ").replace(/\s+/g, " ").trim();
}

function escapeHtml(text: string) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function extractBoxContent($box: cheerio.Cheerio<any>) {
  const content = $box.find("> .tcolorbox-content").first();
  return (content.length ? content.html() : $box.html()) ?? "";
}

function extractHintContent($: cheerio.CheerioAPI, $box: cheerio.Cheerio<any>) {
  const content = $box.find(".mdframed").first();
  const html = (content.length ? content.html() : $box.html()) ?? "";
  return html.replace(
    /<span class=(['"])cmbx-[^'"]+\1>\s*Hint:\s*<\/span>/i,
    "",
  );
}

function normalizeSectionHeadings($: cheerio.CheerioAPI) {
  $("h3.sectionHead").each((_, element) => {
    const id = $(element).attr("id");
    const text = normalizeWhitespace($(element).text());
    const attrs = id ? ` id="${escapeHtml(id)}"` : "";
    $(element).replaceWith(`<h1${attrs}>${escapeHtml(text)}</h1>`);
  });

  $("h4.subsectionHead").each((_, element) => {
    const id = $(element).attr("id");
    const text = normalizeWhitespace($(element).text());
    const attrs = id ? ` id="${escapeHtml(id)}"` : "";
    $(element).replaceWith(`<h2${attrs}>${escapeHtml(text)}</h2>`);
  });

  $("h3.likesectionHead#contents, .tableofcontents").remove();
}

function rebuildProblemSections($: cheerio.CheerioAPI) {
  const $problemsHeading = $("h1#problems").first();
  if (!$problemsHeading.length) {
    return;
  }

  const $solutionsHeading = $("h1#solutions").first();
  const solutionMap = new Map<
    string,
    { solutionHtml: string; takeawaysHtml: string; remarkHtml: string[] }
  >();

  if ($solutionsHeading.length) {
    const $solutionHeadings = $solutionsHeading
      .nextUntil(undefined, "h2")
      .add($solutionsHeading.nextAll("h2"))
      .filter((_, element) =>
        ($(element).attr("id") ?? "").startsWith("solution-to-problem-"),
      );

    $solutionHeadings.each((_, element) => {
      const $heading = $(element);
      const title = normalizeWhitespace($heading.text());
      const problemNumber = title.match(/Problem\s+(\d+)/i)?.[1];
      if (!problemNumber) {
        return;
      }

      const $block = $heading.nextUntil("h1, h2");
      const $solutionBox = $block.filter(".tcolorbox.solutionbox").first();
      const $takeawaysBox = $block.filter(".tcolorbox.takeawaysbox").first();
      const remarkHtml = $block
        .filter(".tcolorbox.remarkbox")
        .toArray()
        .map((node) => $.html(node) ?? "");

      solutionMap.set(problemNumber, {
        solutionHtml: extractBoxContent($solutionBox),
        takeawaysHtml: extractBoxContent($takeawaysBox),
        remarkHtml,
      });
    });
  }

  const $problemHeadings = $problemsHeading
    .nextUntil("h1#solutions", "h2")
    .filter((_, element) => ($(element).attr("id") ?? "").startsWith("problem-"));

  const sections: string[] = [];

  $problemHeadings.each((_, element) => {
    const $heading = $(element);
    const title = normalizeWhitespace($heading.text());
    const sectionId = $heading.attr("id") ?? "";
    const problemNumber = title.match(/Problem\s+(\d+)/i)?.[1] ?? "";
    const $block = $heading.nextUntil("h1, h2");
    const $problemBox = $block.filter(".tcolorbox.problembox").first();
    const $hintBox = $block.filter("div.minipage").first();
    const solutionEntry = solutionMap.get(problemNumber);

    const parts = [
      `<section class="problem-entry"${sectionId ? ` id="${escapeHtml(sectionId)}"` : ""}>`,
      `<h2>${escapeHtml(title)}</h2>`,
    ];

    if ($problemBox.length) {
      parts.push(
        `<section class="problem-part problem-statement"><h3>Problem Statement</h3>${extractBoxContent($problemBox)}</section>`,
      );
    }

    if ($hintBox.length) {
      parts.push(
        `<section class="problem-part problem-hints"><h3>Hints</h3>${extractHintContent($, $hintBox)}</section>`,
      );
    }

    if (solutionEntry?.solutionHtml) {
      parts.push(
        `<section class="problem-part problem-solution"><h3>Solution</h3>${solutionEntry.solutionHtml}${solutionEntry.remarkHtml.join("")}</section>`,
      );
    }

    if (solutionEntry?.takeawaysHtml) {
      parts.push(
        `<section class="problem-part problem-takeaways"><h3>Takeaways</h3>${solutionEntry.takeawaysHtml}</section>`,
      );
    }

    parts.push("</section>");
    sections.push(parts.join(""));
  });

  const rebuiltProblems = [`<h1 id="problems">2 Problems</h1>`, ...sections].join("");

  if ($solutionsHeading.length) {
    $problemsHeading.nextUntil("h1#solutions").remove();
    $solutionsHeading.nextAll().remove();
    $solutionsHeading.remove();
  } else {
    $problemsHeading.nextAll().remove();
  }

  $problemsHeading.replaceWith(rebuiltProblems);
}

export function postprocessHtml(html: string, slug: string) {
  const repairedHtml = repairKnownMake4htArtifacts(html);
  const $ = cheerio.load(repairedHtml);

  $("script, noscript, iframe").remove();
  $("head").remove();
  $("meta, link, title").remove();

  $("[style]").each((_, element) => {
    const current = $(element).attr("style");
    if (!current) {
      return;
    }

    const safe = current
      .split(";")
      .map((part) => part.trim())
      .filter((part) => {
        const lower = part.toLowerCase();
        return (
          lower.startsWith("text-align") ||
          lower.startsWith("margin") ||
          lower.startsWith("padding") ||
          lower.startsWith("width") ||
          lower.startsWith("max-width")
        );
      })
      .join("; ");

    if (safe) {
      $(element).attr("style", safe);
    } else {
      $(element).removeAttr("style");
    }
  });

  $("*").each((_, element) => {
    const attribs =
      "attribs" in element && element.attribs ? element.attribs : {};
    for (const name of Object.keys(attribs)) {
      if (name.startsWith("on")) {
        $(element).removeAttr(name);
      }
    }
  });

  $("img").each((_, element) => {
    const src = $(element).attr("src");
    if (src) {
      $(element).attr("src", rewriteAssetUrl(src, slug));
    }
  });

  $("ul.itemize1").each((_, element) => {
    $(element).addClass("booklet-list booklet-list-bullets");
  });

  $("ul.itemize1 > li.itemize").each((_, element) => {
    $(element).addClass("booklet-list-item");
  });

  $("object, embed").remove();
  normalizeSectionHeadings($);
  rebuildProblemSections($);

  const bodyHtml = $("body").html();
  const mainHtml = bodyHtml ?? $.root().html() ?? "";

  return `
    <article class="booklet-document">
      ${mainHtml}
    </article>
  `.trim();
}
