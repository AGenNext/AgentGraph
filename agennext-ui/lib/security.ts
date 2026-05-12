// Input sanitization utilities
// Production-grade security helpers

/**
 * Sanitize string input to prevent XSS
 */
export function sanitizeString(input: string): string {
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
}

/**
 * Validate email format
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate UUID format
 */
export function isValidUUID(uuid: string): boolean {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  return uuidRegex.test(uuid);
}

/**
 * Validate agent status transitions
 */
export function isValidStatusTransition(
  currentStatus: string,
  newStatus: string
): boolean {
  const allowedTransitions: Record<string, string[]> = {
    draft: ['registered'],
    registered: ['active', 'suspended'],
    active: ['suspended', 'revoked'],
    suspended: ['active', 'revoked'],
    revoked: [],
  };
  
  return allowedTransitions[currentStatus]?.includes(newStatus) ?? false;
}

/**
 * Sanitize for HTML display
 */
export function sanitizeHTML(input: string): string {
  const div = typeof document !== 'undefined' 
    ? document.createElement('div') 
    : null;
  
  if (div) {
    div.textContent = input;
    return div.innerHTML;
  }
  
  // Server-side sanitization
  return sanitizeString(input);
}

/**
 * Validate and sanitize user input
 */
export function validateInput(
  input: string,
  maxLength: number = 500,
  allowedChars?: RegExp
): { valid: boolean; sanitized: string; error?: string } {
  if (!input || typeof input !== 'string') {
    return { valid: false, sanitized: '', error: 'Input required' };
  }
  
  if (input.length > maxLength) {
    return { valid: false, sanitized: '', error: `Max ${maxLength} characters` };
  }
  
  if (allowedChars && !allowedChars.test(input)) {
    return { valid: false, sanitized: '', error: 'Invalid characters' };
  }
  
  return { valid: true, sanitized: input.trim() };
}

/**
 * Rate limiting helper (in-memory for demo)
 */
const rateLimitMap = new Map<string, { count: number; resetAt: number }>();

export function checkRateLimit(
  identifier: string,
  maxRequests: number = 100,
  windowMs: number = 60000
): boolean {
  const now = Date.now();
  const record = rateLimitMap.get(identifier);
  
  if (!record || record.resetAt < now) {
    rateLimitMap.set(identifier, { count: 1, resetAt: now + windowMs });
    return true;
  }
  
  if (record.count >= maxRequests) {
    return false;
  }
  
  record.count++;
  return true;
}