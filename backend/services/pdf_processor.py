"""
PDF processing service for extracting text and analyzing content
"""

import os
import fitz  # PyMuPDF
import pdfplumber
from typing import Dict, List, Tuple
import re
import tempfile
from .ai_artifact_generator import AIArtifactGenerator
from .storage import SupabaseStorage

class PDFProcessor:
    """Process PDF files and extract content for AI analysis"""
    
    def __init__(self):
        api_key = os.environ.get("TOGETHER_API_KEY")
        self.ai_generator = AIArtifactGenerator(anthropic_api_key=api_key)
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        
        text_content = ""
        temp_file = None
        
        try:
            # Check if path is a storage reference (user_id/filename)
            if not os.path.exists(pdf_path) and '/' in pdf_path:
                # It's likely a Supabase storage path - download to temp file
                storage = SupabaseStorage()
                pdf_data = storage.download_file(pdf_path)
                
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                temp_file.write(pdf_data)
                temp_file.close()
                
                # Use the temp file path instead
                pdf_path = temp_file.name
            
            # Try with pdfplumber first (better for structured text)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n\n"
            
            # If pdfplumber didn't extract much, try PyMuPDF
            if len(text_content.strip()) < 100:
                doc = fitz.open(pdf_path)
                text_content = ""
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    text_content += page.get_text() + "\n\n"
                doc.close()
                
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
        finally:
            # Clean up temp file if it exists
            if temp_file and os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
        
        return text_content.strip()
    
    def split_into_chapters(self, text: str) -> List[Tuple[str, str]]:
        """Split text content into logical chapters"""
        
        # Common chapter patterns
        patterns = [
            r'^(Chapter\s+([IVXLCDM]+|\d+))[:\.\s]*(.*?)$',
            r'^(\d+\.\s+.*?)$',
            r'^(Section\s+\d+)[:\.\s]*(.*?)$',
            r'^(Part\s+[IVXLCDM]+|\d+)[:\.\s]*(.*?)$',
            r'^(Introduction|Conclusion|Summary|Appendix|References)[:\.\s]*(.*?)$'
        ]
        
        chapters = []
        lines = text.split('\n')
        current_chapter = ""
        current_title = "Introduction"
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line matches chapter pattern
            is_chapter_start = False
            for pattern in patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    # Save previous chapter
                    if current_chapter.strip():
                        chapters.append((current_title, current_chapter.strip()))
                    
                    # Start new chapter
                    current_title = line
                    current_chapter = ""
                    is_chapter_start = True
                    break
            
            if not is_chapter_start:
                current_chapter += line + "\n"
        
        # Add final chapter
        if current_chapter.strip():
            chapters.append((current_title, current_chapter.strip()))
        
        return chapters if chapters else [("Full Document", text)]
    
    def analyze_content_structure(self, text: str) -> Dict:
        """Analyze PDF content to determine structure and topics"""
        
        analysis = {
            "word_count": len(text.split()),
            "estimated_reading_time": len(text.split()) // 200,  # ~200 words per minute
            "has_mathematical_content": bool(re.search(r'[=+\-*/∑∫∂√π]|equation|formula', text, re.IGNORECASE)),
            "has_logical_content": bool(re.search(r'\b(true|false|and|or|not|boolean|logic)\b', text, re.IGNORECASE)),
            "has_code_content": bool(re.search(r'(def |function |class |import |#include)', text)),
            "chapter_count": len(self.split_into_chapters(text)),
            "complexity_level": self._assess_complexity(text)
        }
        
        return analysis
    
    def _assess_complexity(self, text: str) -> str:
        """Assess the complexity level of the content"""
        
        # Simple heuristics for complexity assessment
        advanced_terms = len(re.findall(r'\b(theorem|lemma|proof|algorithm|optimization|differential|integral)\b', text, re.IGNORECASE))
        sentence_length = len(text.split('.')) / len(text.split('\n')) if text.split('\n') else 0
        
        if advanced_terms > 10 or sentence_length > 15:
            return "advanced"
        elif advanced_terms > 3 or sentence_length > 10:
            return "intermediate"
        else:
            return "beginner"
    
    def process_pdf_for_artifacts(self, pdf_path: str, title: str) -> Dict:
        """Complete PDF processing pipeline for artifact generation"""
        
        try:
            # Extract text
            text_content = self.extract_text_from_pdf(pdf_path)
            if not text_content:
                return {"error": "Could not extract text from PDF"}
            
            # Analyze structure
            analysis = self.analyze_content_structure(text_content)
            
            # Split into chapters
            chapters = self.split_into_chapters(text_content)
            
            # Generate artifacts
            study_guide_code = self.ai_generator.generate_study_guide(text_content, title)
            quiz_code = self.ai_generator.generate_quiz(text_content, title)
            
            return {
                "success": True,
                "text_content": text_content,
                "analysis": analysis,
                "chapters": chapters,
                "artifacts": {
                    "study_guide": study_guide_code,
                    "quiz": quiz_code
                }
            }
            
        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}
