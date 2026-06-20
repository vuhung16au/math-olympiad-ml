const fs = require('fs');

const file = 'lib/booklets.ts';
let content = fs.readFileSync(file, 'utf8');

const universalKeywords = '", "NESA aligned", "past paper practice", "Year 12 Maths", "HSC tutoring alternative"';

content = content.replace(
  /keywords:\s*\[(.*?)\]/g,
  (match, p1) => {
    // If it already has NESA aligned, skip
    if (p1.includes('NESA aligned')) return match;
    
    // Add specific keywords depending on p1
    let specificKeywords = '';
    if (p1.includes('Combinatorics')) {
        specificKeywords = '", "binomial expansion exercises", "HSC Extension 2 counting problems';
    } else if (p1.includes('Mechanics')) {
        specificKeywords = '", "resisted motion HSC questions", "projectile motion worked examples';
    } else if (p1.includes('Mathematical Proof')) {
        specificKeywords = '", "HSC mathematical induction proofs", "proof by contradiction examples';
    } else if (p1.includes('Mixed Problems')) {
        specificKeywords = '", "HSC Maths past papers alternative", "HSC revision questions';
    }

    return `keywords: [${p1}${specificKeywords}${universalKeywords}]`;
  }
);

fs.writeFileSync(file, content);
console.log('Keywords updated successfully');
